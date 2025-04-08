from pydantic import BaseModel, Field


class ScheduleConfiguration(BaseModel):
    """
    Configuration of the schedule of the query.

    Parameters
    ----------
    ScheduleExpression : str
        An expression that denotes when to trigger the scheduled query run.
        This can be a cron expression or a rate expression.
    """

    ScheduleExpression: str = Field(min_length=1, max_length=256)
