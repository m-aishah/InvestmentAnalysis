# Real Estate Investment Tool

## Overview

The Real Estate Investment Tool is an extension designed to help users make informed real estate investment decisions. Built using Flask and deployed on AWS, this tool integrates seamlessly with CMND.ai, providing a range of functionalities to assist users in evaluating properties based on cost, risk, rental income, and overall investment potential.

## Features

### 1. Cost Comparison Tool

- **Description**: Compares the prices of properties within a specified budget range and location.
- **Usage**: Helps users quickly identify properties that match their financial criteria.

### 2. Rental Income Forecast

- **Description**: Provides estimates on potential rental income based on historical data and market trends.
- **Usage**: Assists users in understanding the income potential of a property.

### 3. Risk Analysis

- **Description**: Evaluates various risk factors associated with properties, such as location, market volatility, and developer history.
- **Usage**: Enables users to assess the risk profile of a property before investing.

### 4. Property Details and Insights

- **Description**: Offers detailed information about properties, including developer details, facilities, and historical data.
- **Usage**: Provides comprehensive insights to aid in making informed decisions.

### 5. General Investment Recommendation

- **Description**: Generates tailored investment recommendations based on user preferences and property data.
- **Usage**: Guides users towards properties that align with their investment goals.

## Usage

This tool is designed to integrate seamlessly with CMND.ai to provide users with powerful investment analysis capabilities. Once connected to CMND.ai, the tool leverages the platform’s AI-driven insights to enhance decision-making in real estate investments.

The tool can also be accessed directly via the following URL: [http://13.61.32.149/](http://13.61.32.149/). Here, users can interact with various endpoints that provide specific functionalities:

- **Cost Comparison Tool**: `/api/cost-comparison` (POST)
- **Rental Income Forecast**: `/api/rental-income-forecast` (POST)
- **Risk Analysis**: `/api/risk-analysis` (POST)
- **Property Details and Insights**: `/api/property-details` (POST)
- **General Investment Recommendation**: `/api/investment-recommendation` (POST)

### Technologies Used

- **Python**: Core programming language for backend development.
- **Flask**: Lightweight web framework for creating API endpoints.
- **Pydantic**: Data validation and settings management using Python type annotations.
- **AWS EC2**: Deployed on an Amazon EC2 instance for scalability and reliability.
- **Caddy**: Utilized as a reverse proxy to manage traffic efficiently.
- **CI/CD Pipeline**: Continuous Integration and Continuous Deployment (CI/CD) is set up to automate testing and deployment, ensuring that any updates or changes are deployed seamlessly.

This setup allows the tool to be robust, scalable, and easy to maintain, providing a reliable solution for real estate investment analysis.
