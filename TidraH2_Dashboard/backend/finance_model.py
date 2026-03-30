
def calculate_crf(r, n):
    """
    Calculate Capital Recovery Factor.

    Args:
        r (float): discount rate (e.g., 0.08 for 8%)
        n (int): project lifetime in years

    Returns:
        float: capital recovery factor
    """
    if r == 0:
        return 1 / n
    return (r * (1 + r)**n) / ((1 + r)**n - 1)

def calculate_lcoh(capex, opex, crf, h2_annual_kg):
    """
    Calculate Levelized Cost of Hydrogen (€/kg).

    Args:
        capex (float): total capital investment (EUR)
        opex (float): annual O&M costs (EUR)
        crf (float): capital recovery factor
        h2_annual_kg (float): hydrogen produced per year in kg

    Returns:
        float: LCOH in EUR/kg
    """
    if h2_annual_kg == 0:
        return float('inf')
    return (capex * crf + opex) / h2_annual_kg

def calculate_score(lcoh, reliability):
    """
    Calculate decision score based on LCOH and source reliability.

    Args:
        lcoh (float): levelized cost of hydrogen (€/kg)
        reliability (float): source availability ratio (0–1)

    Returns:
        float: scenario score
    """
    if lcoh == 0:
        return float('inf')
    return 0.6 * (1 / lcoh) + 0.4 * reliability
