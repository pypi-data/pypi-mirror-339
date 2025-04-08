import shutil, ctypes, time, os, zarr, pprint, psutil, dask, copy
import numpy as np, os, glob, tempfile
from multiprocessing.pool import ThreadPool

from dask import array as da
from distributed import LocalCluster, Client
from dask_jobqueue import SLURMCluster
from pathlib import Path
from typing import Union

from eubi_bridge.ngff.multiscales import Pyramid
from eubi_bridge.ngff import defaults
from eubi_bridge.ebridge_base import BridgeBase, VoxelMeta, downscale, abbreviate_units

import logging, warnings

logging.getLogger('distributed.diskutils').setLevel(logging.CRITICAL)

def verify_filepaths_for_cluster(
                             filepaths
                             ):
    print(f"Verifying file extensions for distributed conversion.")
    formats = ['lif', 'czi', 'lsm',
               'ome.tiff', 'ome.tif', 'tiff', 'tif']
    for filepath in filepaths:
        verified = any(list(map(lambda path, ext: path.endswith(ext), [filepath] * len(formats), formats)))
        if not verified:
            root, ext = os.path.splitext(filepath)
            warnings.warn(f"Distributed execution is not supported for the {ext} format")
            warnings.warn(f"Falling back on multithreading.")
            break
    if verified:
        print(f"File extensions were verified for distributed conversion.")
    return verified

class EuBIBridge:
    """
    EuBIBridge is a conversion tool for bioimage datasets, allowing for both unary and aggregative conversion of image
    data collections to OME-Zarr format.

    Attributes:
        config_gr (zarr.Group): Configuration settings stored in a Zarr group.
        config (dict): Dictionary representation of configuration settings for cluster, conversion, and downscaling.
        dask_config (dict): Dictionary representation of configuration settings for dask.distributed.
        root_defaults (dict): Installation defaults of configuration settings for cluster, conversion, and downscaling.
        root_dask_defaults (dict): Installation defaults of configuration settings for dask.distributed.
    """
    def __init__(self,
                 configpath = f"{os.path.expanduser('~')}/.eubi_bridge",
               ):
        """
        Initializes the EuBIBridge class and loads or sets up default configuration.

        Args:
            configpath (str, optional): Path to store configuration settings. Defaults to the home directory.
        """

        root_dask_defaults = {'distributed.adaptive.interval': '1s', 'distributed.adaptive.maximum': '.inf',
             'distributed.adaptive.minimum': 0, 'distributed.adaptive.target-duration': '5s',
             'distributed.adaptive.wait-count': 3, 'distributed.admin.event-loop': 'tornado',
             'distributed.admin.large-graph-warning-threshold': '10MB',
             'distributed.admin.log-format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
             'distributed.admin.log-length': 10000, 'distributed.admin.low-level-log-length': 1000,
             'distributed.admin.max-error-length': 10000, 'distributed.admin.pdb-on-err': False,
             'distributed.admin.system-monitor.disk': True, 'distributed.admin.system-monitor.gil.enabled': True,
             'distributed.admin.system-monitor.gil.interval': '1ms', 'distributed.admin.system-monitor.host-cpu': False,
             'distributed.admin.system-monitor.interval': '500ms', 'distributed.admin.system-monitor.log-length': 7200,
             'distributed.admin.tick.cycle': '1s', 'distributed.admin.tick.interval': '20ms',
             'distributed.admin.tick.limit': '3s', 'distributed.client.heartbeat': '5s',
             'distributed.client.preload': [], 'distributed.client.preload-argv': [],
             'distributed.client.scheduler-info-interval': '2s', 'distributed.client.security-loader': None,
             'distributed.comm.compression': False, 'distributed.comm.default-scheme': 'tcp',
             'distributed.comm.offload': '10MiB', 'distributed.comm.require-encryption': None,
             'distributed.comm.retry.count': 0, 'distributed.comm.retry.delay.max': '20s',
             'distributed.comm.retry.delay.min': '1s', 'distributed.comm.shard': '64MiB',
             'distributed.comm.socket-backlog': 2048, 'distributed.comm.timeouts.connect': '30s',
             'distributed.comm.timeouts.tcp': '30s', 'distributed.comm.tls.ca-file': None,
             'distributed.comm.tls.ciphers': None, 'distributed.comm.tls.client.cert': None,
             'distributed.comm.tls.client.key': None, 'distributed.comm.tls.max-version': None,
             'distributed.comm.tls.min-version': 1.2, 'distributed.comm.tls.scheduler.cert': None,
             'distributed.comm.tls.scheduler.key': None, 'distributed.comm.tls.worker.cert': None,
             'distributed.comm.tls.worker.key': None, 'distributed.comm.ucx.create-cuda-context': None,
             'distributed.comm.ucx.cuda-copy': None, 'distributed.comm.ucx.environment': {},
             'distributed.comm.ucx.infiniband': None, 'distributed.comm.ucx.nvlink': None,
             'distributed.comm.ucx.rdmacm': None, 'distributed.comm.ucx.tcp': None,
             'distributed.comm.websockets.shard': '8MiB', 'distributed.comm.zstd.level': 3,
             'distributed.comm.zstd.threads': 0, 'distributed.dashboard.export-tool': False,
             'distributed.dashboard.graph-max-items': 5000,
             'distributed.dashboard.link': '{scheme}://{host}:{port}/status',
             'distributed.dashboard.prometheus.namespace': 'dask', 'distributed.deploy.cluster-repr-interval': '500ms',
             'distributed.deploy.lost-worker-timeout': '15s',
             'distributed.diagnostics.computations.ignore-files': ['runpy\.py', 'pytest', 'py\.test',
                                                                   'pytest-script\.py', '_pytest', 'pycharm',
                                                                   'vscode_pytest', 'get_output_via_markers\.py'],
             'distributed.diagnostics.computations.ignore-modules': ['asyncio', 'functools', 'threading', 'datashader',
                                                                     'dask', 'debugpy', 'distributed', 'coiled', 'cudf',
                                                                     'cuml', 'matplotlib', 'pluggy', 'prefect',
                                                                     'rechunker', 'xarray', 'xgboost', 'xdist',
                                                                     '__channelexec__', 'execnet'],
             'distributed.diagnostics.computations.max-history': 100, 'distributed.diagnostics.computations.nframes': 0,
             'distributed.diagnostics.cudf': False, 'distributed.diagnostics.erred-tasks.max-history': 100,
             'distributed.diagnostics.nvml': True, 'distributed.nanny.environ': {},
             'distributed.nanny.pre-spawn-environ.MALLOC_TRIM_THRESHOLD_': 65536,
             'distributed.nanny.pre-spawn-environ.MKL_NUM_THREADS': 1,
             'distributed.nanny.pre-spawn-environ.OMP_NUM_THREADS': 1,
             'distributed.nanny.pre-spawn-environ.OPENBLAS_NUM_THREADS': 1, 'distributed.nanny.preload': [],
             'distributed.nanny.preload-argv': [], 'distributed.p2p.comm.buffer': '1 GiB',
             'distributed.p2p.comm.concurrency': 10, 'distributed.p2p.comm.message-bytes-limit': '2 MiB',
             'distributed.p2p.comm.retry.count': 10, 'distributed.p2p.comm.retry.delay.max': '30s',
             'distributed.p2p.comm.retry.delay.min': '1s', 'distributed.p2p.storage.buffer': '100 MiB',
             'distributed.p2p.storage.disk': True, 'distributed.p2p.threads': None, 'distributed.rmm.pool-size': None,
             'distributed.scheduler.active-memory-manager.interval': '2s',
             'distributed.scheduler.active-memory-manager.measure': 'optimistic',
             'distributed.scheduler.active-memory-manager.policies': [
                 {'class': 'distributed.active_memory_manager.ReduceReplicas'}],
             'distributed.scheduler.active-memory-manager.start': True, 'distributed.scheduler.allowed-failures': 3,
             'distributed.scheduler.allowed-imports': ['dask', 'distributed'],
             'distributed.scheduler.bandwidth': '100000000', 'distributed.scheduler.blocked-handlers': [],
             'distributed.scheduler.contact-address': None,
             'distributed.scheduler.dashboard.bokeh-application.allow_websocket_origin': ['*'],
             'distributed.scheduler.dashboard.bokeh-application.check_unused_sessions_milliseconds': 500,
             'distributed.scheduler.dashboard.bokeh-application.keep_alive_milliseconds': 500,
             'distributed.scheduler.dashboard.status.task-stream-length': 1000,
             'distributed.scheduler.dashboard.tasks.task-stream-length': 100000,
             'distributed.scheduler.dashboard.tls.ca-file': None, 'distributed.scheduler.dashboard.tls.cert': None,
             'distributed.scheduler.dashboard.tls.key': None, 'distributed.scheduler.default-data-size': '1kiB',
             'distributed.scheduler.default-task-durations.rechunk-split': '1us',
             'distributed.scheduler.default-task-durations.split-shuffle': '1us',
             'distributed.scheduler.default-task-durations.split-stage': '1us',
             'distributed.scheduler.default-task-durations.split-taskshuffle': '1us',
             'distributed.scheduler.events-cleanup-delay': '1h',
             'distributed.scheduler.http.routes': ['distributed.http.scheduler.prometheus',
                                                   'distributed.http.scheduler.info', 'distributed.http.scheduler.json',
                                                   'distributed.http.health', 'distributed.http.proxy',
                                                   'distributed.http.statics'],
             'distributed.scheduler.idle-timeout': None, 'distributed.scheduler.locks.lease-timeout': '30s',
             'distributed.scheduler.locks.lease-validation-interval': '10s',
             'distributed.scheduler.no-workers-timeout': None, 'distributed.scheduler.preload': [],
             'distributed.scheduler.preload-argv': [], 'distributed.scheduler.rootish-taskgroup': 5,
             'distributed.scheduler.rootish-taskgroup-dependencies': 5,
             'distributed.scheduler.unknown-task-duration': '500ms', 'distributed.scheduler.validate': False,
             'distributed.scheduler.work-stealing': True, 'distributed.scheduler.work-stealing-interval': '1s',
             'distributed.scheduler.worker-saturation': 1.1, 'distributed.scheduler.worker-ttl': '5 minutes',
             'distributed.version': 2, 'distributed.worker.blocked-handlers': [],
             'distributed.worker.connections.incoming': 10, 'distributed.worker.connections.outgoing': 50,
             'distributed.worker.daemon': True,
             'distributed.worker.http.routes': ['distributed.http.worker.prometheus', 'distributed.http.health',
                                                'distributed.http.statics'],
             'distributed.worker.lifetime.duration': None, 'distributed.worker.lifetime.restart': False,
             'distributed.worker.lifetime.stagger': '0 seconds', 'distributed.worker.memory.max-spill': False,
             'distributed.worker.memory.monitor-interval': '100ms', 'distributed.worker.memory.pause': 0.8,
             'distributed.worker.memory.rebalance.measure': 'optimistic',
             'distributed.worker.memory.rebalance.recipient-max': 0.6,
             'distributed.worker.memory.rebalance.sender-min': 0.3,
             'distributed.worker.memory.rebalance.sender-recipient-gap': 0.1,
             'distributed.worker.memory.recent-to-old-time': '30s', 'distributed.worker.memory.spill': 0.7,
             'distributed.worker.memory.spill-compression': 'auto', 'distributed.worker.memory.target': 0.6,
             'distributed.worker.memory.terminate': 0.95, 'distributed.worker.memory.transfer': 0.1,
             'distributed.worker.multiprocessing-method': 'spawn', 'distributed.worker.preload': [],
             'distributed.worker.preload-argv': [], 'distributed.worker.profile.cycle': '1000ms',
             'distributed.worker.profile.enabled': True, 'distributed.worker.profile.interval': '10ms',
             'distributed.worker.profile.low-level': False, 'distributed.worker.resources': {},
             'distributed.worker.transfer.message-bytes-limit': '50MB', 'distributed.worker.use-file-locking': True,
             'distributed.worker.validate': False
        }

        defaults = dict(
            cluster = dict(
                n_jobs=4,
                threads_per_worker=1,
                memory_limit='auto',
                temp_dir='auto',
                no_worker_restart=False,
                verbose=False,
                no_distributed=False,
                on_slurm = False,
            ),
            conversion = dict(
                output_chunks = (1, 1, 256, 256, 256),
                compressor = 'blosc',
                compressor_params = {},
                overwrite = False,
                use_tensorstore=False,
                rechunk_method='auto',
                rechunkers_max_mem = "auto",
                trim_memory=False,
                metadata_reader = 'bfio',
                save_omexml = True,
            ),
            downscale = dict(
                scale_factor=(1, 1, 2, 2, 2),
                n_layers=3,
                downscale_method='simple',
            )
        )

        self.root_defaults = defaults
        self.root_dask_defaults = root_dask_defaults
        config_gr = zarr.open_group(configpath, mode = 'a')
        config = config_gr.attrs
        for key in defaults.keys():
            if key not in config.keys():
                config[key] = {}
                for subkey in defaults[key].keys():
                    if subkey not in config[key].keys():
                        config[key][subkey] = defaults[key][subkey]
            config_gr.attrs[key] = config[key]
        self.config = dict(config_gr.attrs)
        ###
        if not 'dask_config' in config_gr.keys():
            config_gr.create_group('dask_config')
        dask_config = config_gr.dask_config.attrs
        for key in root_dask_defaults.keys():
            if key not in dask_config.keys():
                dask_config[key] = root_dask_defaults[key]
        config_gr.dask_config.attrs.update(dict(dask_config))
        self.dask_config = dict(config_gr.dask_config.attrs)
        self.config_gr = config_gr
        ###
        self._dask_temp_dir = None
        self.client = None

    def reset_config(self):
        """
        Resets the cluster, conversion and downscale parameters to the installation defaults.
        """
        self.config_gr.attrs.update(self.root_defaults)
        self.config = dict(self.config_gr.attrs)

    def reset_dask_config(self):
        """
        Resets the dask configuration parameters to the installation defaults.
        """
        self.config_gr.dask_config.attrs.update(self.root_dask_defaults)
        self.dask_config = dict(self.config_gr.dask_config.attrs)

    def show_config(self):
        """
        Displays the current cluster, conversion, and downscale parameters.
        """
        pprint.pprint(self.config)

    def show_dask_config(self):
        """
        Displays the current dask.distributed parameters.
        """
        pprint.pprint(self.dask_config)

    def show_root_defaults(self):
        """
        Displays the installation defaults for cluster, conversion, and downscale parameters.
        """
        pprint.pprint(self.root_defaults)

    def show_root_dask_defaults(self):
        """
        Displays the installation defaults for dask.distributed.
        """
        pprint.pprint(self.root_dask_defaults)

    def _collect_params(self, param_type, **kwargs):
        """
        Gathers parameters from the configuration, allowing for overrides.

        Args:
            param_type (str): The type of parameters to collect (e.g., 'cluster', 'conversion', 'downscale').
            **kwargs: Parameter values that may override defaults.

        Returns:
            dict: Collected parameters.
        """
        params = {}
        for key in self.config[param_type].keys():
            if key in kwargs.keys():
                params[key] = kwargs[key]
            else:
                params[key] = self.config[param_type][key]
        return params

    # def _collect_scales(self, **kwargs):
    #     """
    #     Retrieves pixel sizes for image dimensions.
    #
    #     Args:
    #         **kwargs: Pixel sizes for time, channel, z, y, and x dimensions.
    #
    #     Returns:
    #         list: Pixel sizes.
    #     """
    #     t = kwargs.get('time_scale', None)
    #     c = kwargs.get('channel_scale', None)
    #     y = kwargs.get('y_scale', None)
    #     x = kwargs.get('x_scale', None)
    #     z = kwargs.get('z_scale', x)
    #     return [t,c,z,y,x]
    #
    # def _collect_units(self, **kwargs):
    #     """
    #     Retrieves unit specifications for image dimensions.
    #
    #     Args:
    #         **kwargs: Unit values for time, channel, z, y, and x dimensions.
    #
    #     Returns:
    #         list: Unit values.
    #     """
    #     t = kwargs.get('time_unit', None)
    #     c = kwargs.get('channel_unit', None)
    #     y = kwargs.get('y_unit', None)
    #     x = kwargs.get('x_unit', None)
    #     z = kwargs.get('z_unit', x)
    #     return [t, c, z, y, x]

    def configure_cluster(self,
                          memory_limit: str = 'default',
                          n_jobs: int = 'default',
                          no_worker_restart: bool = 'default',
                          on_slurm: bool = 'default',
                          temp_dir: str = 'default',
                          threads_per_worker: int = 'default',
                          no_distributed: bool = 'default',
                          verbose: bool = 'default'
                         ):
        """
        Updates cluster configuration settings. To update the current default value for a parameter, provide that parameter with a value other than 'default'.

        The following parameters can be configured:
            - memory_limit (str, optional): Memory limit per worker.
            - n_jobs (int, optional): Number of parallel jobs.
            - no_worker_restart (bool, optional): Whether to prevent worker restarts.
            - on_slurm (bool, optional): Whether running on a SLURM cluster.
            - temp_dir (str, optional): Temporary directory for Dask workers.
            - threads_per_worker (int, optional): Number of threads per worker.
            - verbose (bool, optional): Enables detailed logging.

        Args:
            memory_limit (str, optional): Memory limit per worker.
            n_jobs (int, optional): Number of parallel jobs.
            no_worker_restart (bool, optional): Whether to prevent worker restarts.
            on_slurm (bool, optional): Whether running on a SLURM cluster.
            temp_dir (str, optional): Temporary directory for Dask workers.
            threads_per_worker (int, optional): Number of threads per worker.
            verbose (bool, optional): Enables detailed logging.

        Returns:
            None
        """

        params = {
            'memory_limit': memory_limit,
            'n_jobs': n_jobs,
            'no_worker_restart': no_worker_restart,
            'on_slurm': on_slurm,
            'temp_dir': temp_dir,
            'threads_per_worker': threads_per_worker,
            'no_distributed': no_distributed,
            'verbose': verbose
        }

        for key in params:
            if key in self.config['cluster'].keys():
                if params[key] != 'default':
                    self.config['cluster'][key] = params[key]
        self.config_gr.attrs['cluster'] = self.config['cluster']

    def configure_conversion(self,
                             compressor: str = 'default',
                             compressor_params: dict = 'default',
                             output_chunks: list = 'default',
                             overwrite: bool = 'default',
                             rechunk_method: str = 'default',
                             rechunkers_max_mem: str = 'default',
                             trim_memory: bool = 'default',
                             use_tensorstore: bool = 'default',
                             metadata_reader: str = 'default',
                             save_omexml: bool = 'default'
                             ):
        """
        Updates conversion configuration settings. To update the current default value for a parameter, provide that parameter with a value other than 'default'.

        The following parameters can be configured:
            - compressor (str, optional): Compression algorithm.
            - compressor_params (dict, optional): Parameters for the compressor.
            - output_chunks (list, optional): Chunk size for output.
            - overwrite (bool, optional): Whether to overwrite existing data.
            - rechunk_method (str, optional): Method used for rechunking.
            - rechunkers_max_mem (str, optional): Maximum memory used by the 'rechunker' tool. Needed only when the 'rechunk_method' is specified as 'rechunker'.
            - trim_memory (bool, optional): Whether to trim memory usage.
            - use_tensorstore (bool, optional): Whether to use TensorStore for writing.
            - save_omexml (bool, optional): Whether to create a METADATA.ome.xml file.
        Args:
            compressor (str, optional): Compression algorithm.
            compressor_params (dict, optional): Parameters for the compressor.
            output_chunks (list, optional): Chunk size for output.
            overwrite (bool, optional): Whether to overwrite existing data.
            rechunk_method (str, optional): Method used for rechunking.
            rechunkers_max_mem (str, optional): Maximum memory used by the 'rechunker' tool. Needed only when the 'rechunk_method' is specified as 'rechunker'.
            trim_memory (bool, optional): Whether to trim memory usage.
            use_tensorstore (bool, optional): Whether to use TensorStore for storage.
            save_omexml (bool, optional): Whether to create a METADATA.ome.xml file.

        Returns:
            None
        """

        params = {
            'compressor': compressor,
            'compressor_params': compressor_params,
            'output_chunks': output_chunks,
            'overwrite': overwrite,
            'rechunk_method': rechunk_method,
            'rechunkers_max_mem': rechunkers_max_mem,
            'trim_memory': trim_memory,
            'use_tensorstore': use_tensorstore,
            'metadata_reader': metadata_reader,
            'save_omexml': save_omexml
        }

        for key in params:
            if key in self.config['conversion'].keys():
                if params[key] != 'default':
                    self.config['conversion'][key] = params[key]
        self.config_gr.attrs['conversion'] = self.config['conversion']

    def configure_downscale(self,
                            downscale_method: str = 'default',
                            n_layers: int = 'default',
                            scale_factor: list = 'default'
                            ):
        """
        Updates downscaling configuration settings. To update the current default value for a parameter, provide that parameter with a value other than 'default'.

        The following parameters can be configured:
            - downscale_method (str, optional): Downscaling algorithm.
            - n_layers (int, optional): Number of downscaling layers.
            - scale_factor (list, optional): Scaling factors for each dimension.

        Args:
            downscale_method (str, optional): Downscaling algorithm.
            n_layers (int, optional): Number of downscaling layers.
            scale_factor (list, optional): Scaling factors for each dimension.

        Returns:
            None
        """

        params = {
            'downscale_method': downscale_method,
            'n_layers': n_layers,
            'scale_factor': scale_factor
        }

        for key in params:
            if key in self.config['downscale'].keys():
                if params[key] != 'default':
                    self.config['downscale'][key] = params[key]
        self.config_gr.attrs['downscale'] = self.config['downscale']

    def _set_dask_temp_dir(self, temp_dir = 'auto'):
        if self._dask_temp_dir is not None:
            self._dask_temp_dir.cleanup()
        if temp_dir in ('auto', None):
            temp_dir = tempfile.TemporaryDirectory()
        else:
            os.makedirs(temp_dir, exist_ok=True)
            temp_dir = tempfile.TemporaryDirectory(dir=temp_dir)
        self._dask_temp_dir = temp_dir
        return self

    def _start_cluster(self,
                    n_jobs: int = 4,
                    threads_per_worker: int = 1,
                    memory_limit: str = 'auto',
                    temp_dir='auto',
                    verbose = False,
                    on_slurm = False,
                    no_distributed = False,
                    config_kwargs = {},
                    **kwargs
                    ):

        config_dict = copy.deepcopy(self.dask_config)
        config_dict.update(**config_kwargs)

        # worker_options = {
        #     "memory_target_fraction": 0.8,
        #     "memory_spill_fraction": 0.9,
        #     "memory_pause_fraction": 0.95,
        #     # "memory_terminate_fraction": 0.98
        # }
        scheduler_options = {
            "allowed_failures": 100,
            "idle_timeout": "1h",
            "worker_ttl": "1d"  # Set to a large value, e.g., 1 day
        }

        self._set_dask_temp_dir(temp_dir)

        dask.config.set(config_dict) # use dictionary notation here.

        if no_distributed:
            config_dict.update(scheduler = 'threads',
                               pool = ThreadPool(n_jobs)
                               )
            dask.config.set(config_dict)
            print(f"Conversion running locally via multithreading.")
        else:
            if memory_limit == 'auto':
                reserve_fraction = kwargs.get('reserve_memory_fraction', 0.1)
                min_per_worker = kwargs.get('min_memory_per_worker', 1 * 1024 ** 3)

                total_mem = psutil.virtual_memory().total
                reserved_mem = total_mem * reserve_fraction
                available_mem = max(0, total_mem - reserved_mem)
                mem_per_worker = max(available_mem / n_jobs, min_per_worker)
                mem_gb = mem_per_worker / (1 * 1024 ** 3)
                memory_limit = f"{mem_gb} GB"
                print(f"{memory_limit} memory has been allocated per worker.")

            if on_slurm:
                print(f"Conversion running on Slurm.")
                cluster = SLURMCluster(
                                        cores=threads_per_worker,
                                        processes=1,
                                        nanny=False,
                                        scheduler_options=scheduler_options,
                                        n_workers=n_jobs,
                                        memory=memory_limit,
                                        local_directory=f"{self._dask_temp_dir.name}",
                                        # **worker_options
                                        )
            else:
                print(f"Conversion running on local cluster.")
                cluster = LocalCluster(
                                       n_workers=n_jobs,
                                       threads_per_worker=threads_per_worker,
                                       # processes=True,
                                       nanny = False,
                                       scheduler_kwargs=scheduler_options,
                                       memory_limit = memory_limit,
                                       local_directory=f"{self._dask_temp_dir.name}",  # Unique directory per worker
                                       # **worker_options
                                       )
            cluster.scale(n_jobs)
            self.client = Client(cluster)
            if verbose:
                print(self.client.cluster)
        return self

    def to_zarr(self,
                input_path: Union[Path, str],
                output_path: Union[Path, str],
                includes=None,
                excludes=None,
                series: int = None,
                time_tag: Union[str, tuple] = None,
                channel_tag: Union[str, tuple] = None,
                z_tag: Union[str, tuple] = None,
                y_tag: Union[str, tuple] = None,
                x_tag: Union[str, tuple] = None,
                concatenation_axes: Union[int, tuple, str] = None,
                save_omexml: bool = None,
                **kwargs
                ):
        """
        Converts image data to OME-Zarr format and optionally applies downscaling.

        Args:
            input_path (Union[Path, str]): Path to input file or directory.
            output_path (Union[Path, str]): Directory, in which the output OME-Zarrs will be written.
            includes (str, optional): Filename patterns to filter for.
            excludes (str, optional): Filename patterns to filter against.
            time_tag (Union[str, tuple], optional): Time dimension tag.
            channel_tag (Union[str, tuple], optional): Channel dimension tag.
            z_tag (Union[str, tuple], optional): Z dimension tag.
            y_tag (Union[str, tuple], optional): Y dimension tag.
            x_tag (Union[str, tuple], optional): X dimension tag.
            concatenation_axes (Union[int, tuple, str], optional): Axes, along which the images will be concatenated.
            **kwargs: Additional configuration overrides.

        Raises:
            Exception: If no files are found in the input path.

        Prints:
            Process logs including conversion and downscaling time.

        Returns:
            None
        """
        t0 = time.time()

        # Get parameters:
        self.cluster_params = self._collect_params('cluster', **kwargs)
        self.conversion_params = self._collect_params('conversion', **kwargs)
        self.downscale_params = self._collect_params('downscale', **kwargs)

        print(f"Base conversion initiated.")
        ###### Handle input data and metadata
        if os.path.isfile(input_path):
            paths = [input_path]
        else:
            if not '*' in input_path:
                input_path_ = os.path.join(input_path, '**')
            else:
                input_path_ = input_path
            paths = glob.glob(input_path_, recursive=True)

        paths = list(filter(lambda path: (includes in path if includes is not None else True)
                                         and
                                         (excludes not in path if excludes is not None else True),
                            paths
                            )
                     )

        filepaths = sorted(list(filter(os.path.isfile, paths)))

        ###### Start the cluster
        verified_for_cluster = verify_filepaths_for_cluster(filepaths) ### Ensure non-bioformats conversion. If bioformats is needed, fall back on local conversion.
        if not verified_for_cluster:
            self.cluster_params['no_distributed'] = True

        self._start_cluster(**self.cluster_params)

        ###### Read and concatenate
        base = BridgeBase(input_path,
                        excludes=excludes,
                        includes=includes,
                        series=series
                        )

        base.read_dataset(verified_for_cluster)

        base.digest(
            time_tag = time_tag,
            channel_tag = channel_tag,
            z_tag = z_tag,
            y_tag = y_tag,
            x_tag = x_tag,
            axes_of_concatenation = concatenation_axes
            )

        pixel_meta_kwargs = {'series': series,
                             'metadata_reader': self.conversion_params['metadata_reader'],
                             **kwargs
                             }
        base.compute_pixel_metadata(**pixel_meta_kwargs)

        verbose = self.cluster_params['verbose']

        # self._start_cluster(**self.cluster_params)

        if 'region_shape' in kwargs.keys():
            self.conversion_params['region_shape'] = kwargs.get('region_shape')
        if verbose:
            print(f"Cluster params:")
            pprint.pprint(self.cluster_params)
            print(f"Conversion params:")
            pprint.pprint(self.conversion_params)
            print(f"Downscale params:")
            pprint.pprint(self.downscale_params)

        temp_dir = base._dask_temp_dir
        self.conversion_params['temp_dir'] = temp_dir
        self.downscale_params['temp_dir'] = temp_dir

        if self.client is not None:
            base.client = self.client
        base.set_dask_temp_dir(self._dask_temp_dir)

        ###### Write
        self.base_results = base.write_arrays(output_path,
                                           # pixel_sizes=scales, ### TODO: scaledict with paths
                                           # pixel_units=units, ### TODO: unitdict with paths
                                           compute=True,
                                           verbose=verbose,
                                           **self.conversion_params
                                           )
        ###### Downscale
        print(f"Base conversion finished.")
        t1 = time.time()
        print(f"Elapsed for base conversion: {(t1 - t0) / 60} min.")
        n_layers = self.downscale_params['n_layers']
        if n_layers > 1:
            print(f"Downscaling initiated.")
            _ = downscale(
                      self.base_results,
                      **self.downscale_params,
                      rechunk_method = 'p2p',
                      verbose = verbose
                      )

            print(f"Downscaling finished.")

        ###### Shutdown and clean up
        if self.client is not None:
            self.client.shutdown()
            self.client.close()

        if isinstance(self._dask_temp_dir, tempfile.TemporaryDirectory):
            shutil.rmtree(self._dask_temp_dir.name)
        else:
            shutil.rmtree(self._dask_temp_dir)

        ###### Write OME metadata
        if save_omexml is None:
            save_omexml = self.conversion_params['save_omexml']
        if save_omexml:
            print(f"Writing OME-XML")
            for key, vmeta in base.flatome.items():
                # arr = base.flatarrays[key]
                # vmeta.set_shape[base.axes, arr.shape]
                vmeta.save_omexml(key)

        t1 = time.time()
        print(f"Elapsed for conversion + downscaling: {(t1 - t0) / 60} min.")


# vmeta = VoxelMeta(f"/home/oezdemir/Desktop/TIM2025/data/example_images/pff/FtsZ2-1_GFP_KO2-1_no10G.lsm")

# vmeta = VoxelMeta(f"/home/oezdemir/PycharmProjects/dask_env2/EuBI-Bridge_tests/blueredchannels_timeseries/Blue-T0002.tif")
# vmeta.ensure_omexml_fields()

# vmeta.set_shape('tz', (1, 91))
# vmeta.set_scales('tz', (1, 1))
#
# essential_fields = {
#     "physical_size_x", "physical_size_x_unit",
#     "physical_size_y", "physical_size_y_unit",
#     "physical_size_z", "physical_size_z_unit",
#     "time_increment", "time_increment_unit",
#     "size_x", "size_y", "size_z", "size_t", "size_c"
# }
#
# # Ensure all essential fields are in model_fields_set
# missing_fields = essential_fields - vmeta.pixel_meta.model_fields_set
# vmeta.pixel_meta.model_fields_set.update(missing_fields)
#
# pprint.pprint(vmeta.omemeta.to_xml())
# vmeta.pixel_meta.model_fields_set.add('physical_size_z_unit')