"""
ammonia_engine.py
-----------------
Chemical equilibrium engine for un-ionized ammonia (NH3) computation.

Based on the thermodynamic model by:
    Emerson, K., Russo, R. C., Lund, R. E., & Thurston, R. V. (1975).
    Aqueous ammonia equilibrium calculations: Effect of pH and temperature.
    Journal of the Fisheries Research Board of Canada, 32(12), 2379-2383.

Formula:
    pKa  = 0.09018 + (2729.92 / (273.15 + T))
    f    = 1 / (1 + 10^(pKa - pH))
    NH3  = TAN * f

Toxicity thresholds (mg/L NH3):
    Safe          : NH3 < 0.02
    Caution       : 0.02 <= NH3 < 0.05
    Critical Toxic: NH3 >= 0.05
"""

import math
import time


# ---------------------------------------------------------------------------
# Toxicity level constants
# ---------------------------------------------------------------------------
LEVEL_SAFE     = "Safe"
LEVEL_CAUTION  = "Caution"
LEVEL_CRITICAL = "Critical Toxic"

THRESHOLD_SAFE    = 0.02   # mg/L
THRESHOLD_CAUTION = 0.05   # mg/L

# Validation ranges (paper Section 1.5)
PH_MIN, PH_MAX     = 6.0, 9.0
TEMP_MIN, TEMP_MAX = 15.0, 35.0
TAN_MIN, TAN_MAX   = 0.0, 10.0


class AmmoniaResult:
    """Holds all outputs of a single NH3 calculation."""

    def __init__(self, tan, ph, temperature, pka, fraction, nh3,
                 toxicity, dosing_instructions, inference_ms):
        self.tan = tan
        self.ph = ph
        self.temperature = temperature
        self.pka = pka
        self.fraction = fraction          # fraction of TAN that is NH3 (0-1)
        self.nh3 = nh3                    # un-ionized ammonia in mg/L
        self.toxicity = toxicity          # LEVEL_SAFE / LEVEL_CAUTION / LEVEL_CRITICAL
        self.dosing_instructions = dosing_instructions  # list[str]
        self.inference_ms = inference_ms  # computation time in milliseconds

    def to_dict(self):
        return {
            "tan":         self.tan,
            "ph":          self.ph,
            "temperature": self.temperature,
            "pka":         round(self.pka, 6),
            "fraction":    round(self.fraction, 6),
            "nh3":         round(self.nh3, 6),
            "toxicity":    self.toxicity,
        }


class AmmoniaEngine:
    """
    Stateless computation engine.
    All methods are class-level so no instantiation is required,
    but the class is kept for clear module organisation.
    """

    # ------------------------------------------------------------------
    # Step-by-step sub-calculations (exposed for testing / Chapter 3)
    # ------------------------------------------------------------------

    @staticmethod
    def compute_pka(temperature_c: float) -> float:
        """
        Compute the temperature-dependent pKa of ammonium ion.

        pKa = 0.09018 + (2729.92 / (273.15 + T))

        Args:
            temperature_c: Water temperature in degrees Celsius.

        Returns:
            pKa value (dimensionless).
        """
        return 0.09018 + (2729.92 / (273.15 + temperature_c))

    @staticmethod
    def compute_fraction_nh3(pka: float, ph: float) -> float:
        """
        Compute the fraction of TAN present as un-ionized NH3.

        f = 1 / (1 + 10^(pKa - pH))

        Args:
            pka: Temperature-dependent pKa.
            ph:  Water pH.

        Returns:
            NH3 fraction in range [0, 1].
        """
        return 1.0 / (1.0 + math.pow(10.0, pka - ph))

    @staticmethod
    def compute_nh3(tan: float, fraction: float) -> float:
        """
        Compute un-ionized ammonia concentration.

        NH3 (mg/L) = TAN * f

        Args:
            tan:      Total Ammonia Nitrogen in mg/L.
            fraction: NH3 fraction from compute_fraction_nh3.

        Returns:
            NH3 concentration in mg/L.
        """
        return tan * fraction

    @staticmethod
    def classify_toxicity(nh3: float) -> str:
        """
        Classify toxicity level from NH3 concentration.

        Args:
            nh3: Un-ionized ammonia concentration in mg/L.

        Returns:
            One of LEVEL_SAFE, LEVEL_CAUTION, or LEVEL_CRITICAL.
        """
        if nh3 < THRESHOLD_SAFE:
            return LEVEL_SAFE
        elif nh3 < THRESHOLD_CAUTION:
            return LEVEL_CAUTION
        else:
            return LEVEL_CRITICAL

    @staticmethod
    def generate_dosing_instructions(nh3: float, toxicity: str,
                                     tan: float, ph: float,
                                     temperature_c: float) -> list:
        """
        Generate step-by-step chemical dosing / maintenance instructions
        based on the calculated toxicity level.

        Returns:
            List of instruction strings.
        """
        instructions = []

        if toxicity == LEVEL_SAFE:
            instructions = [
                "Water condition is SAFE -- no immediate action required.",
                "Perform routine 10-20% water change weekly.",
                "Continue monitoring TAN, pH, and temperature weekly.",
                "Maintain biological filtration to keep TAN near 0 mg/L.",
            ]

        elif toxicity == LEVEL_CAUTION:
            instructions = [
                "CAUTION -- un-ionized ammonia is approaching toxic threshold.",
                f"Current NH3: {nh3:.4f} mg/L -- target below 0.02 mg/L.",
                "Perform an immediate 25-30% partial water change.",
                "Reduce feeding to decrease nitrogenous waste output.",
                "Check and clean mechanical filter media.",
                "Retest TAN, pH, and temperature after 24 hours.",
                "Consider adding an ammonia-neutralising conditioner (e.g., Prime).",
            ]

        else:  # LEVEL_CRITICAL
            instructions = [
                "CRITICAL TOXIC -- immediate intervention required!",
                f"Current NH3: {nh3:.4f} mg/L -- EXCEEDS safe limit of 0.02 mg/L.",
                "Perform an emergency 40-50% water change NOW.",
                "Temporarily stop all feeding.",
                "Add ammonia detoxifier / conditioner immediately.",
                "Check pH -- reducing pH lowers NH3 fraction; target pH 7.0.",
                f"At current pH {ph:.1f} and {temperature_c:.1f} deg C, "
                f"lowering pH by 0.5 units reduces NH3 by ~{100*(1 - 1/(1+math.pow(10, AmmoniaEngine.compute_pka(temperature_c)-(ph-0.5)))/AmmoniaEngine.compute_fraction_nh3(AmmoniaEngine.compute_pka(temperature_c), ph)):.1f}%.",
                "Move fish to a holding tank if NH3 exceeds 0.10 mg/L.",
                "Retest every 6 hours until Safe level is reached.",
                "Review stocking density and feeding regime.",
            ]

        return instructions

    # ------------------------------------------------------------------
    # Main entry point
    # ------------------------------------------------------------------

    @staticmethod
    def calculate(tan: float, ph: float, temperature_c: float) -> AmmoniaResult:
        """
        Full pipeline: validate inputs, compute NH3, classify, generate
        dosing instructions, and record inference time.

        Args:
            tan:           Total Ammonia Nitrogen (mg/L), range 0-10.
            ph:            Water pH, range 6.0-9.0.
            temperature_c: Water temperature (degC), range 15-35.

        Returns:
            AmmoniaResult object with all computed values.

        Raises:
            ValueError: If any input is outside its valid range.
        """
        # --- Input validation -------------------------------------------
        if not (TAN_MIN <= tan <= TAN_MAX):
            raise ValueError(
                f"TAN must be between {TAN_MIN} and {TAN_MAX} mg/L. Got {tan}."
            )
        if not (PH_MIN <= ph <= PH_MAX):
            raise ValueError(
                f"pH must be between {PH_MIN} and {PH_MAX}. Got {ph}."
            )
        if not (TEMP_MIN <= temperature_c <= TEMP_MAX):
            raise ValueError(
                f"Temperature must be between {TEMP_MIN} and {TEMP_MAX} degC. "
                f"Got {temperature_c}."
            )

        # --- Computation pipeline (timed) --------------------------------
        t_start = time.perf_counter()

        pka      = AmmoniaEngine.compute_pka(temperature_c)
        fraction = AmmoniaEngine.compute_fraction_nh3(pka, ph)
        nh3      = AmmoniaEngine.compute_nh3(tan, fraction)
        toxicity = AmmoniaEngine.classify_toxicity(nh3)
        dosing   = AmmoniaEngine.generate_dosing_instructions(
                       nh3, toxicity, tan, ph, temperature_c)

        t_end = time.perf_counter()
        inference_ms = (t_end - t_start) * 1000.0

        return AmmoniaResult(
            tan=tan,
            ph=ph,
            temperature=temperature_c,
            pka=pka,
            fraction=fraction,
            nh3=nh3,
            toxicity=toxicity,
            dosing_instructions=dosing,
            inference_ms=inference_ms,
        )
