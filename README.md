# dockerstache
Mustache templated dockerfile builder

Given a directory containing Dockerfile's and script templates this tool lets you parametrize them out using [mustache](http://mustache.github.io/) compatible templating and then renders them using a context provided as a json file. 
The package contains a CLI that does a basic directory structure clone and template render from an initial starting directory containing templates to a copy that contains the rendedered templates suitable for running docker build and docker run commands. 

## Installation 

Install via pip:

```bash 
pip install dockerstache
```

## Example

Given a directory structure like:

```
docker_templates/
  Dockerfile.mustache 
  install.sh.mustache
  scripts/
      setup.sh.mustache
      run.py.mustache 
```

And a context file containing the subsitition variables as a json dictionary, the following command will 
render all the mustache templates into the same directory structure under the output directory:

```
dockerstache -i ./docker_templates -o ./docker_output/ -c context.json
```

Resulting in a directory structure like:

```
docker_templates/
  Dockerfile
  install.sh
  scripts/
      setup.sh
      run.py

```

If for example the dockerfile.mustache template contains {{name}} then the context.json should contain a name attribute at the top level. The context data is passed directly to the [pystache](https://github.com/defunkt/pystache) renderer. 
