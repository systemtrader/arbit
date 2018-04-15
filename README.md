# arbit

Arbit has been an effort to apply some sort of statistical arbitrage to the equity and futures markets.  

## History
The original code was in Mathematica, written during a Christmas vacation in 2006.  It was ported to Matlab and later Python.  I moved it to python3 well before that was a viable language, back in the Python 3K days.  At one point it had a network bootable OS image and ran on a small cluster under a desk in my London apartment.  

There was a brief, glorious, period in there around 2008 where the API integration to TD Ameritrade all worked and the model (Naive Bayes with a lot of featurization logic) was spitting out predictions with high confidence that netted $1-2k/day.  Then the market changed and prediction confidence plunged.

Sometime after that, the code was modified to use Oracle and I had to custom build the cx_Oracle driver.  By 2015, it used python3, mongodb and ran on AWS.  It also included a little PHP and d3 visualization.

During 2016, I rewrote it to use GCP BigQuery and AppEngine.  At the time there were a lot of issues with the BigQuery driver and it seemed like pure serverless wasn't quite there as AppEngine was missing various language features and isn't serverless anyway.  The goal at the time was to use Cloud ML and Cloud Datalab.  In 2018, Cloud Functions looked like a solution but they're still in beta and only support node.js.

## Roadmap
In November 2017, AWS came out with Sagemaker.  Between that, S3, Lambda and Athena, it seems like giving the AWS ecosystem a try is in order.  I'm going to try to port everything there.

First off, I'm going to do some work to size the data volume and make sure I don't accidentally spend $100k/month...

* Google Drive - [Arbit](https://drive.google.com/open?id=1GocLSCYCmF52XVj9gMokjTZNxCbrsHfv)
* Google Sheet - [Arbit - Cost Analysis](https://docs.google.com/spreadsheets/d/1Tqnlqs20LnuvpxmK2S-3PH58dGlq5k-4G2KZ-V5jbcs/edit?usp=sharing)

# Setup

First off, you're going to need a local copy of this repo:

    git clone https://github.com/benofben/arbit.git
    cd arbit

You'll also need to install and configure the AWS CLI:

    pip install --upgrade --user awscli
    aws configure

You can make sure that the CLI is working by running:

    aws ec2 describe-regions

Next, you'll need a role to create lambdas, etc.  To create that run:

    aws iam create-role \
      --role-name arbit_role \
      --assume-role-policy-document file://arbit_role.json

You'll need to grab the role_arn from there.  Be sure to paste it at the top of `arbit/downloader/setup.sh`
