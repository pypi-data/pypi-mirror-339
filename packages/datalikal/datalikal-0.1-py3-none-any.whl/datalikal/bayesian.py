# bayesian.py



import math

def bayesian_update(prior_alpha, prior_beta, successes, failures):
    """Perform a Bayesian update for a Beta distribution."""
    posterior_alpha = prior_alpha + successes
    posterior_beta = prior_beta + failures
    return posterior_alpha, posterior_beta

def beta_pdf(alpha, beta, x):
    """Compute the probability density function of the Beta distribution."""
    if x < 0 or x > 1:
        return 0
    numerator = (x ** (alpha - 1)) * ((1 - x) ** (beta - 1))
    denominator = beta_function(alpha, beta)
    return numerator / denominator

def beta_function(alpha, beta):
    """Compute the Beta function B(alpha, beta)."""
    return gamma(alpha) * gamma(beta) / gamma(alpha + beta)

def gamma(n):
    """Compute the Gamma function using recursion for integers or approximation for non-integers."""
    if n == 1:
        return 1
    elif n == 0.5:
        return math.sqrt(math.pi)
    else:
        return (n - 1) * gamma(n - 1)

def bayesian_inference(data, mu_prior=0, sigma_prior=1, observed_sigma=1):
    """Perform Bayesian inference for a normal distribution with known variance."""
    n = len(data)
    mean_observed = sum(data) / n
    posterior_variance = 1 / (1 / sigma_prior**2 + n / observed_sigma**2)
    posterior_mean = posterior_variance * (mu_prior / sigma_prior**2 + n * mean_observed / observed_sigma**2)
    posterior_std = math.sqrt(posterior_variance)
    return posterior_mean, posterior_std

def bayesian_hypothesis_testing(prior_odds, likelihood_ratio):
    """Perform Bayesian hypothesis testing."""
    posterior_odds = prior_odds * likelihood_ratio
    return posterior_odds

def credible_interval(alpha, beta, confidence_level=0.95):
    """Compute the credible interval for a Beta distribution using a simple approximation."""
    mean = alpha / (alpha + beta)
    variance = (alpha * beta) / ((alpha + beta) ** 2 * (alpha + beta + 1))
    std_dev = math.sqrt(variance)
    z = 1.96  # Approximate for 95% confidence
    lower_bound = max(0, mean - z * std_dev)
    upper_bound = min(1, mean + z * std_dev)
    return lower_bound, upper_bound

def posterior_predictive(prior_alpha, prior_beta, observed_data):
    """Compute the posterior predictive distribution for new data."""
    successes = sum(observed_data)
    failures = len(observed_data) - successes
    posterior_alpha, posterior_beta = bayesian_update(prior_alpha, prior_beta, successes, failures)
    return {
        "success": posterior_alpha / (posterior_alpha + posterior_beta),
        "failure": posterior_beta / (posterior_alpha + posterior_beta),
    }

def bayesian_credible_region(data, mu_prior, sigma_prior, observed_sigma, confidence=0.95):
    """Compute a credible region for Bayesian inference."""
    posterior_mean, posterior_std = bayesian_inference(data, mu_prior, sigma_prior, observed_sigma)
    z = 1.96  # Approximation for 95% confidence interval
    lower_bound = posterior_mean - z * posterior_std
    upper_bound = posterior_mean + z * posterior_std
    return lower_bound, upper_bound


