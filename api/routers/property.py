import aiof.property.core as property

from fastapi import APIRouter

from aiof.data.property import MortgageCalculatorRequest


router = APIRouter()


@router.post("/mortgage")
async def mortgage_calc(req: MortgageCalculatorRequest):
    return property.mortgage_calc(
        property_value              = req.propertyValue,
        down_payment                = req.downPayment,
        interest_rate               = req.interestRate,
        loan_term_years             = req.loanTermYears,
        start_date                  = req.startDate,
        pmi                         = req.pmi,
        property_insurance          = req.propertyInsurance,
        monthly_hoa                 = req.monthlyHoa,
        include_yearly_breakdown    = True,
        as_json                     = True)