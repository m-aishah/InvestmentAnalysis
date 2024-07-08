from modules.cost_comparison import run_cost_comparison_module
from modules.future_projections import run_future_projections_module
# from modules.risk_analysis import run_risk_analysis_module
# from modules.property_details_and_insights import run_property_details_and_insights
# from modules.rental_income_analysis import run_rental_income_analysis
# from modules.investment_recommendation  import run_investment_recommendation_wrapper
from models import InvestmentOptionsSchema, custom_json_schema

# Define the tool configuration and metadata for CMND.ai
tools = [
    {
        "name": "cost_comparison_module",
        "description": "Filters and compares investment options based on user-defined criteria & Costs",
        "parameters": custom_json_schema(InvestmentOptionsSchema),
        "runCmd": run_cost_comparison_module,
        "isDangerous": False,
        "functionType": "backend",
        "isLongRunningTool": False,
        "rerun": True,
        "rerunWithDifferentParameters": True
    },

    {
        "name": "future_projections_module",
        "description": "Calculates expected return and potential revenue for investment options",
        "parameters": None,
        "runCmd": run_future_projections_module,
        "isDangerous": False,
        "functionType": "backend",
        "isLongRunningTool": False,
        "rerun": True,
        "rerunWithDifferentParameters": False
    }

   # {
    #    "name": "investment_recommendations_module",
     #   "description": "Provides investment recommendations based on predefined criteria",
      #  "parameters": None,  # No parameters needed for this module
       # "runCmd": run_investment_recommendations_module,
#        "isDangerous": False,
 #       "functionType": "backend",
  #      "isLongRunningTool": False,
   #     "rerun": True,
    #    "rerunWithDifferentParameters": False
    #}    
]