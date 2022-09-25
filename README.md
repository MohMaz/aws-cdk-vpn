
# Development 

## Install python requirements

```
make virtualenv
source .venv/bin/activate
make install-dev

```

## Install CDK CLI
```
npm install -g aws-cdk@latest
```

## Deploy

```
cdk synth
cdk diff
# Check the diff log
cdk deploy
```