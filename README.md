# AWS API Gateway Assessment

## Summary

This project implement an AWS infrastructure using CloudFormation to provision:

<ol>
    <li>Amazon Cognito for authentication</li>
    <li>API Gateway with two secured endpoint</li>
    <li>
        Two Lambda function calling public APIs which are
            <ol>
                <li>Open Weather Map API</li>
                <li>Exchange Rate API</li>
            </ol>
    </li>
</ol>

## Table Of Contents

- [Architecture Overview](#architecture-overview)
- [Repository Structure](#repository-structure)
- [Repository Structure](#repository-structure)
- [Notes](#notes)
- [Cloning Repository](#clone-this-repository)
- [Deployment Instructions](#deployment-instructions)
- [Cognito Setup](#cognito-setup)
- [API Testing](#api-testing)
- [Lambda Sample Payloads](#lambda-sample-payloads)

## Architecture Overview

```
Client → API Gateway (secured with Cognito)
├── /weather → Lambda1 (Node.js, OpenWeather API)
└── /exchange → Lambda2 (Python, ExchangeRate API)
```
- Lambda1 calls OpenWeatherMap to fetch weather info for a given city
- Lambda2 calls [open.er-api.com](https://open.er-api.com/v6/latest/USD) to fetch exchange rates

## Repository Structure
```
/aws-api-gateway-assessment
├── README.md
├── cloudformation
│   └── main.yaml
├── lambdas
│   ├── lambda1
│   │   └── index.js
│   └── lambda2
│       └── lambda_function.py
│   └── lambda1.zip // pre-zipped for easier deployment
│   └── lambda2.zip // pre-zipped for easier deployment
├── assets
│   ├── sc1.png
│   ├── sc2.png
│   ├── sc3.png
```
## Notes
- This assessment uses AWS Free Tier.
- Lambda1 uses node-fetch, Lambda2 uses urllib.request
- Cognito authentication required for both endpoints

## Clone This repository

```
git clone https://github.com/HtunHtunHtet/aws-api-gateway-assessment.git
cd aws-api-gateway-assessment
```

## Deployment Instructions
### Pre-requisites

- AWS CLI installed and configured
- AWS Web Interface access
- Access to an AWS account with CloudFormation, Lambda, API Gateway, and Cognito permissions
- Your own S3 bucket containing the zipped Lambda code (lambda1.zip, lambda2.zip)
- Get free API key for open weather [here](https://openweathermap.org/api)

### 1. Upload Lambda Zips file to S3

#### 1.1 Create Bucket
```
aws s3 mb s3://my-api-assessment-bucket  
```

#### 1.2 Upload Lambda Zips to S3
```
aws s3 cp lambdas/lambda1.zip s3://my-api-assessment-bucket/lambda1.zip
aws s3 cp lambdas/lambda2.zip s3://my-api-assessment-bucket/lambda2.zip
```

### 2. Deploy CloudFormation

```
aws cloudformation deploy \
  --template-file cloudformation/main.yaml \
  --stack-name api-gateway-cognito-assessment \
  --capabilities CAPABILITY_NAMED_IAM \
  --parameter-overrides OpenWeatherApiKey=YOUR_OPENWEATHER_API_KEY
```

NOTE: Remember to change `YOUR_OPENWEATHER_API_KEY` to your own open weather API key. Get your api key [here](https://openweathermap.org/api).

## Cognito Setup
### 1. Get User Pool Id from below command
```
aws cognito-idp list-user-pools --max-results 10
```

### 2. Create user
```
aws cognito-idp admin-create-user \
  --user-pool-id <USER_POOL_ID> \
  --username test@test.com \
  --user-attributes Name=email,Value=test@test.com \
  --temporary-password TempPass123! \
  --message-action SUPPRESS
  
aws cognito-idp admin-set-user-password \
  --user-pool-id <USER_POOL_ID> \
  --username test@test.com \
  --password YourSecurePassword123! \
  --permanent
```

### 3. Get Client ID

```
aws cognito-idp list-user-pool-clients \
  --user-pool-id <USER_POOL_ID> \
  --query "UserPoolClients[*].ClientId" \
  --output text
```


### 4. Update The App Client to Enable the Auth Flow:

If you don't update the app client to enable the auth flow, you won't be able to get JWT ID token. 
So perform below steps to enable the auth flow:

- Go to the [Cognito Console](https://console.aws.amazon.com/cognito/)
- Click your User Pool (i.e `MyUserPool`)
- Go to the `App clients` tab 
- Click your App Client
![sc1.png](assets%2Fsc1.png)
- Go to `Edit`
![sc2.png](assets%2Fsc2.png)
- Enable "Sign in with username and password: ALLOW_USER_PASSWORD_AUTH"
![sc3.png](assets%2Fsc3.png)
- Save Change

### 5. Get JWT ID Token

```
aws cognito-idp initiate-auth \
  --auth-flow USER_PASSWORD_AUTH \
  --client-id <CLIENT_ID> \
  --auth-parameters USERNAME=test@test.com,PASSWORD=YourSecurePassword123!
```

NOTE: 
- Change `<CLIENT_ID>` with the ID that you get from step 3.
- Don't forget to perform [Step 4 above](#4-update-the-app-client-to-enable-the-auth-flow) before this step

Expected return result 

```json
{
    "ChallengeParameters": {},
    "AuthenticationResult": {
        "AccessToken": "",
        "ExpiresIn": 3600,
        "TokenType": "Bearer",
        "RefreshToken": "",
        "IdToken": "" //  This is our JWT ID token 
    }
}
```

## API Testing


### 1. Get your API gateway id

```
aws apigateway get-rest-apis \
  --query "items[?name=='MySecuredApi'].id" \
  --output text
```

### 2. Call Weather API 

```
curl -H "Authorization: <ID_TOKEN>" \
  "https://<api-gateway-id>.execute-api.<region>.amazonaws.com/prod/weather?city=London"
```

- Update your `<ID_TOKEN>` form [Cognito Setup , step 5](#5-get-jwt-id-token),
- Get your API gateway id [from above step](#1-get-your-api-gateway-id) and update it in `<api-gateway-id>`
- Update <region> with your region that cloud formation is deployed
- run it.

For example : it is going to be something like below

```
curl -H "Authorization: <ID_TOKEN>" \
  "https://on5fx53pjd.execute-api.us-east-1.amazonaws.com/prod/weather?city=Calgary"
```
Expected result 

```json
{"temperature":289.28,"weather":"overcast clouds"}
```

### 3. Call Exchange Rate API

```
url -H "Authorization: <ID_TOKEN>" \
  "https://<api-id>.execute-api.<region>.amazonaws.com/prod/exchange?base={your_base_currency}&target={your_target_currency}"
```

- Update your ID_TOKEN form [Cognito Setup , step 5](#5-get-jwt-id-token),
- Get your API gateway id [from above step](#1-get-your-api-gateway-id)
- run it.

For example : it is going to be something like below

```
curl -H "Authorization: <ID_TOKEN>” \
  "https://on5fx53pjd.execute-api.us-east-1.amazonaws.com/prod/exchange?base=CAD&target=SGD"
```

Expected Result

```json
{"base": "CAD", "target": "SGD", "rate": 0.933697}
```

## Lambda Sample Payloads
### Lambda1 (`/weather`)

```json
{
  "queryStringParameters": {
    "city": "London"
  }
}
```
```json
{
  "queryStringParameters": {
    "base": "USD",
    "target": "EUR"
  }
}
```