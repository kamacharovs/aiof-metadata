import aiof.goal.core as goal

from aiof.data.goal import GoalAnalyzeRequest

from fastapi import APIRouter


router = APIRouter()


@router.post("/analyze")
async def goal_analyze_async(req: GoalAnalyzeRequest):
    return goal.analyze(
        goal                = req.goal, 
        current_goals       = req.currentGoals,
        current_assets      = req.currentAssets,
        current_liabilities = req.currentLiabilities)