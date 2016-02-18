# dockerstache
Mustache templated dockerfile builder

[![Build Status](https://travis-ci.org/evansde77/dockerstache.svg?branch=develop)](https://travis-ci.org/evansde77/dockerstache)

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

## .dockerstache 

You can set default options and enable features like pre and post scripts via a .dockerstache file in the template directory. This file is a json file containing several option fields and if it exists in the input template directory, will be read and used as part of the rendering process. CLI options will override settings in the .dockerstache file. 

The following fields are supported:

 * pre_script - Name of a script in the template dir to run prior to rendering templates
 * post_script - Name of a script in the template dir to run post rendering of templates
 * context - Context file name (same as CLI option)
 * defaults - Default file name (same as CLI option)
 * output - Output directory (same as CLI option)


## Pre and Post scripts

dockerstache 0.0.8 and onwards support pre and post execution scripts which can be added to the template directory and flagged in the .dockerstache file. 
Scripts should be added to the template dir and made executable. 
You can then reference them in the .dockerstache file and they will be run by the dockerstache command. 

Example .dockerstache file:

```json
{
  "pre_script": "pre.sh",
  "post_script": "post.sh"
}
```

This will cause dockerstache to look for pre.sh in the template directory and execute it before it renders the templates, 
and after rendering will look for post.sh in the template directory and execute it. 
The scripts are executed in the template directory, and the environment will contain the options from the dockerstache command prefixed with DOCKERSTACHE_<option name> to allow for pre generation of defaults or contexts for example in the expected locations. 

An example with trivial scripts can be found in the [test/templates](https://github.com/evansde77/dockerstache/tree/develop/test/templates) directory of this package.



