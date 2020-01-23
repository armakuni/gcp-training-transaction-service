# Transaction Services

### Transaction service for handling the transaction published by the Casher service. This application will be auto invoked when Cashier service push the transaction message in pubsubtop

### Installation

#### Set environment variables
BALANCE_NAMESPACE
ENV
PORT=5002(default)
APP_NAME=Balance Service App(default)
ACCOUNTS_SERVICE_URL = Account Service end point to get account information. default="http://localhost:5001/accounts/"
BALANCE_TOPIC_ID = Balancer service topic name where Transaction service will publish the latest balance for the account.environ.get("BALANCE_TOPIC", "balance")

#### Requirements

- A Firestore instance up and running in your Google Cloud account
- A Google service account to access the Firestore and PubSub

#### To Create Firestore instance

- [Goto the Firestore page on your console](https://console.cloud.google.com/firestore/data)
- From the Select a database service screen, choose Cloud Firestore in Native mode.
- Select a location for your Cloud Firestore.

#### To Create service account

- Login to your Google Cloud account using google sso

```bash
gcloud auth login
```

- Create service account
* Service account Naming convention: Must be between 6 and 30 characters (inclusive), must begin with a lowercase letter,
and consist of lowercase alphanumeric characters that can be separated by hyphens.

```bash
gcloud iam service-accounts create [NAME]
```

```bash
gcloud projects add-iam-policy-binding [PROJECT_ID] --member "serviceAccount:[NAME]@[PROJECT_ID].iam.gserviceaccount.com" --role "roles/datastore.user"
```

```bash
gcloud iam service-accounts keys create [FILE_NAME].json --iam-account [NAME]@[PROJECT_ID].iam.gserviceaccount.com
```

- Provide authentication credentials to this application code by setting the environment variable GOOGLE_APPLICATION_CREDENTIALS.

```bash
export GOOGLE_APPLICATION_CREDENTIALS="[PATH_TO_CREDENTIALS_JSON_FILE]"
```

e.g export GOOGLE_APPLICATION_CREDENTIALS="/home/user/Downloads/[FILE_NAME].json"

# DO NOT STORE THE CREDENTIALS FILE INSIDE THE REPOSITORY

It is strongly recommended not to store the credentials in the repository as this might lead to a security risk. Unless the file is encrypted, it could be exposed when pushed up if the repository is public,
or if the repository is used to create a container image which is stored publicly. There are best practices around storing secrets which are explained in 205-handling-secrets-during-app-deployment

#### Refer below link for more detail about setting up the environment to use google Firestore

- https://cloud.google.com/firestore/docs/quickstart-servers

### Set env variables


### To run linter

```bash
make lint
```

### To run tests

```bash
make tests
```

### To run the service

```bash
make run
```

### Deployment

```bash
gcloud builds submit --substitutions=_TRANSACTION_NAMESPACE="[TRANSACTION_NAMESPACE]",_BALANCE_TOPIC_ID="[BALANCE_TOPIC_ID]",_ACCOUNTS_SERVICE_URL="[ACCOUNTS_SERVICE_URL]"
```

### API documentation

You can access the API documentation by launching the application and visiting [swagger ui](http://localhost:5002/docs/)
