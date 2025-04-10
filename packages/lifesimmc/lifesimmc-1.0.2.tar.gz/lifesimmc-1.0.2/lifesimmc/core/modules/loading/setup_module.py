from typing import overload

from phringe.core.entities.configuration import Configuration
from phringe.core.entities.instrument import Instrument
from phringe.core.entities.observation import Observation
from phringe.core.entities.scene import Scene
from phringe.main import PHRINGE

from lifesimmc.core.modules.base_module import BaseModule
from lifesimmc.core.resources.config_resource import ConfigResource


class SetupModule(BaseModule):
    """Class representation of the configuration loader module.

    Parameters
    ----------
    n_config_out : str
        Name of the output configuration resource.
    configuration : Configuration
        Configuration object.
    observation : Observation
        Observation object.
    instrument : Instrument
        Instrument object.
    scene : Scene
        Scene object.
    """

    @overload
    def __init__(self, n_config_out: str, configuration: Configuration):
        """Constructor method.

        Parameters
        ----------
        n_config_out : str
            The name of the output configuration resource
        configuration : Configuration
            The configuration object
        """
        ...

    @overload
    def __init__(
            self,
            n_config_out: str,
            observation: Observation,
            instrument: Instrument,
            scene: Scene
    ):
        """Constructor method.

        Parameters
        ----------
        n_config_out : str
            The name of the output configuration resource
        observation : Observation
            The observation mode object
        instrument : Instrument
            The instrument object
        scene : Scene
            The scene object
        """
        ...

    def __init__(
            self,
            n_config_out: str,
            configuration: Configuration = None,
            observation: Observation = None,
            instrument: Instrument = None,
            scene: Scene = None
    ):
        """Constructor method.

        Parameters
        ----------
        n_config_out : str
            The name of the output configuration resource
        configuration : Configuration
            The configuration object
        observation : Observation
            The observation mode object
        instrument : Instrument
            The instrument object
        scene : Scene
            The scene object
        """
        super().__init__()
        self.n_config_out = n_config_out
        self.configuration = configuration
        self.observation = observation
        self.instrument = instrument
        self.scene = scene

    def apply(self, resources: list[ConfigResource]) -> ConfigResource:
        """Load the configuration file.

        Parameters
        ----------
        resources : list[ConfigResource]
            List of resources.

        Returns
        -------
        ConfigResource
            The configuration resource.
        """
        print('Loading configuration...')
        phringe = PHRINGE(
            seed=self.seed,
            gpu_index=self.gpu_index,
            grid_size=self.grid_size,
            time_step_size=self.time_step_size,
            device=self.device,
            extra_memory=40
        )

        if self.configuration:
            phringe.set(self.configuration)

        if self.instrument:
            phringe.set(self.instrument)

        if self.observation:
            phringe.set(self.observation)

        if self.scene:
            phringe.set(self.scene)

        r_config_out = ConfigResource(
            name=self.n_config_out,
            phringe=phringe,
            configuration=self.configuration,
            instrument=phringe._instrument,
            observation=phringe._observation,
            scene=phringe._scene,
        )

        print('Done')
        return r_config_out
