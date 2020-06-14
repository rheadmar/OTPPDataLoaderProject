# OTPPDataLoaderProject
This tracks the OTPPDataLoader Project which is meant to take data from the following two sources:

https://www.alphavantage.co

https://finnhub.io/

It uses a server client architecture to try and create a signal generator that could be used to invest on.

This currently requires you to set up a conda environment and run the scripts from that environment.

This uses the anaconda packages for environment management found here: https://anaconda.org/conda-forge/pandas
setting up an environment for conda should involve running some commands that look like the follwoing:

<code>
  conda create --name myenv --file env.yml
  
  activate myenv
 </code>

In this case myenv is something you can specify but env.yml is the file located in the root directory of this project. 

The following two commands will provide help and instructions that specify how the command parameters available on startup of the two scripts provided for starting up the server and client.

<code>python server.py -h </code>

<code>python client.py -h </code>
