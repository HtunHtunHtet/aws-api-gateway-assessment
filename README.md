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

## 📐 Architecture Overview

```
Client → API Gateway (secured with Cognito)
├── /weather → Lambda1 (Node.js, OpenWeather API)
└── /exchange → Lambda2 (Python, ExchangeRate API)
```
<ul>
    <li>Lambda1 calls OpenWeatherMap to fetch weather info for a given city</li>
    <li>Lambda2 calls open.er-api.com to fetch exchange rates </li>
</ul>


## 🚀 Deployment Instructions
### Pre-requisites
<ul>
    <li>AWS CLI installed and configured</li>
    <li>Access to an AWS account with CloudFormation, Lambda, API Gateway, and Cognito permissions</li>
    <li>Your own S3 bucket containing the zipped Lambda code (lambda1.zip, lambda2.zip)</li>
</ul>

### 1. Upload Lambda Zips file to S3

#### 1.1 Create Bucket
```
aws s3 mb s3://my-api-assessment-bucket  
```

#### 1.2 Upload Lambda Zips to S3
```
aws s3 cp lambda1.zip s3://my-api-assessment-bucket/lambdas/lambda1.zip
aws s3 cp lambda2.zip s3://my-api-assessment-bucket/lambdas/lambda2.zip
```