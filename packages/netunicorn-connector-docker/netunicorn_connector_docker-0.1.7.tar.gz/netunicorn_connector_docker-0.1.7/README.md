# netunicorn-connector-docker
This is a netunicorn connector for a local Docker infrastructure.


This connector works only with the local Docker daemon, requires current user to be in the docker group
and always presents a single host with the name "dockerhost".

## Usage
This connector is supposed to be installed as a part of netunicorn-director-infrastructure package or container.

Install the package:
```bash
pip install netunicorn-connector-docker
```
Ensure that the user (netunicorn-director-infrastructure process owner) is in the docker group (or root).

Then, add the connector to the netunicorn-director-infrastructure configuration:
```yaml
  local-docker:  # unique name
    enabled: true
    module: "netunicorn.director.infrastructure.connectors.docker_connector"  # where to import from
    class: "DockerConnector"  # class name
    config: "configuration-example.yaml"     # path to configuration file
```