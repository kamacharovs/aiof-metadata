import datetime

from pydantic import BaseModel
from typing import Optional


class FiTime(BaseModel):
    startingAmount: Optional[float] = None
    monthlyInvestment: Optional[float] = None
    desiredYearsExpensesForFi: Optional[int] = None
    desiredAnnualSpending: Optional[float] = None

class FiRuleOf72(BaseModel):
    startingAmount: Optional[float] = None
    interest: Optional[float] = None

class FiAddedTime(BaseModel):
    monthlyInvestment: Optional[float] = None
    totalAdditionalExpense: Optional[float] = None

class FiCompoundInterest(BaseModel):
    startingAmount: Optional[float] = None
    monthlyInvestment: Optional[float] = None
    interest: Optional[float] = None
    numberOfYears: Optional[int] = None
    investmentFees: Optional[float] = None
    taxDrag: Optional[float] = None

class FiInvestmentFeesEffect(BaseModel):
    ageAtCareerStart: Optional[int] = None
    interestReturnWhileWorking: Optional[float] = None
    interestReturnWhileRetired: Optional[float] = None
    taxDrag: Optional[float] = None
    annualSavingsFirstDecade: Optional[float] = None
    annualSavingsSecondDecade: Optional[float] = None
    annualWithdrawalThirdDecade: Optional[float] = None

class FiRaisingChildren(BaseModel):
    annualExpensesStart: Optional[float] = None
    annualExpensesIncrement: Optional[float] = None
    children: Optional[list] = None
    interests: Optional[list] = None

class SavingsRate(BaseModel):
    salary: Optional[float] = None
    matchAndProfitSharing: Optional[float] = None
    federalIncomeTax: Optional[float] = None
    stateIncomeTax: Optional[float] = None
    fica: Optional[float] = None
    healthAndDentalInsurance: Optional[float] = None
    otherDeductibleBenefits: Optional[float] = None
    hsaInvestment: Optional[float] = None
    fourOhOneKOrFourOhThreeB: Optional[float] = None
    fourFiveSevenB: Optional[float] = None
    sepIra: Optional[float] = None
    otherTaxDeferred: Optional[float] = None
    rothIra: Optional[float] = None
    taxableAccount: Optional[float] = None
    education: Optional[float] = None
    mortgagePrincipal: Optional[float] = None
    studentLoanPrincipal: Optional[float] = None
    otherPostTaxInvestment: Optional[float] = None
    currentNestEgg: Optional[float] = None


class BmiImperial(BaseModel):
    weight: float
    feet: float
    inches: float

class BmiMetric(BaseModel):
    weight: float
    height: float


class CoastFireSavings(BaseModel):
    age: int                            # Age
    year: datetime                      # Year
    contribution: float                 # Yearly contribution
    yearlyReturn: float                 # Yearly return in %
    total: Optional[float]
    initialEarning: Optional[float]
    withdrawFour: Optional[float]
    withdrawThree: Optional[float]
    withdrawTwo: Optional[float]
    presentValueFour: Optional[float]
    presentValueThree: Optional[float]
    presentValueTwo: Optional[float]
