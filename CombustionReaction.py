from Molecule import Molecule

class Reaction:
    fuel: Molecule
    O2 = Molecule(formula="O2")
    H2O = Molecule(formula="H2O")
    CO = Molecule(formula="CO")
    CO2 = Molecule(formula="CO2")
    N2 = Molecule(formula="N2")

    fuel_in = 0
    O2_in = 0
    H2O_out = 0
    CO_out = 0
    CO2_out = 0

    _initial_temperature = 300 # K

    def _simplifyReaction(self):
        """Reduce the reaction equation as far as possible"""
        canBeSimplified = True
        while canBeSimplified:
            canBeSimplified = False
            primeNumbers = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59]
            # Should only need 2 how it is currently written (limited by fuel_in = 4)
            for divisor in primeNumbers:
                numerators = [self.fuel_in, self.O2_in, self.H2O_out, self.CO_out, self.CO2_out]
                min = numerators[0]
                for numerator in numerators:
                    if numerator > 0 and numerator < min:
                        min = numerator
                if divisor > min:
                    break
                allDivisible = True
                for numerator in numerators:
                    if numerator % divisor != 0:
                        allDivisible = False
                        break
                if allDivisible:
                    self.fuel_in //= divisor
                    self.O2_in //= divisor
                    self.H2O_out //= divisor
                    self.CO_out //= divisor
                    self.CO2_out //= divisor
                    canBeSimplified = True

    @property
    def airFuelRatio(self):
        """The mass ratio of air to fuel for this reaction"""
        massOfFuelReacted = self.fuel_in * self.fuel.molarMass
        return self._mass_air / massOfFuelReacted
    
    @property
    def enthalpy_out(self):
        """(kJ/mol) The enthalpy released by this reaction"""
        return self.fuel_in * self.fuel.enthalpy + self.O2_in * Reaction.O2.enthalpy - (
            self.H2O_out * Reaction.H2O.enthalpy + self.CO2_out * Reaction.CO2.enthalpy + \
            self.CO_out * Reaction.CO.enthalpy)
    
    @property
    def entropy_start(self):
        """((J/K)/mol) The entropy before this reaction"""
        return self.fuel_in * self.fuel.entropy + self.O2_in * Reaction.O2.entropy
    @property
    def entropy_end(self):
        """((J/K)/mol) The entropy after this reaction"""
        return self.H2O_out * Reaction.H2O.entropy + self.CO2_out * Reaction.CO2.entropy + \
            self.CO_out * Reaction.CO.entropy
    @property
    def entropy_change(self):
        """((J/K)/mol) The change in entropy during this reaction"""
        return self.entropy_end - self.entropy_start

    @property
    def _mass_air(self):
        """(g) The mass of air required for 1 mol of this Reaction"""
        airDensity = 0.001225
        volumeRatioOfO2InAir = 0.209
        O2 = Reaction.O2
        massRatioOfO2InAir = volumeRatioOfO2InAir * O2.density / airDensity
        return self.O2_in * O2.molarMass / massRatioOfO2InAir


    @property 
    def cv_temperature_change(self):
        """
        (K) The temperature change of this reaction at constant volume

        ***Assumption*** This is a combustion reaction in Earth's atmosphere
        """
        heat_capacity = Reaction.CO2._specificHeat * self.CO2_out * Reaction.CO2.molarMass + (
            Reaction.CO._specificHeat * self.CO_out * Reaction.CO.molarMass + 
            Reaction.H2O._specificHeat * self.H2O_out * Reaction.H2O.molarMass + 
            Reaction.N2._specificHeat * 0.79 * self._mass_air) # ((J/K)/mol)
        return -self._initial_temperature * self.entropy_change / (
            heat_capacity - self.entropy_end / 2.)
        # That - sign isn't in my derivation, but the magnitude seems right...

    @property
    def usable_energy(self):
        """(kJ/mol) The amount of usable energy released by this reaction"""
        # heatEnergy = (self._initial_temperature + self.cv_temperature_change / 2.) * self.entropy_change
        # ^ This one makes more sense to me ^
        heatEnergy = (self._initial_temperature + self.cv_temperature_change) * self.entropy_change
        # Rough estimate
        print(f"temperature change: {self.cv_temperature_change:2f} K")
        # return self.enthalpy_out - heatEnergy / 1000.
        # ^ This one makes more sense to me ^
        return self.enthalpy_out + heatEnergy / 1000.

    @property
    def power(self):
        """
        (kJ/50LAir) The power potential of this reaction
        Value should represent the kW of chemical power available to a 1L engine at 6000RPM
        (or the hp of chemical power available to a 1L engine at 4478RPM)
        """
        airDensity = 0.001225
        volumeRatioOfO2InAir = 0.209
        CCAirUsed = self.O2_in * Reaction.O2.molarMass / (Reaction.O2.density * volumeRatioOfO2InAir)
        return self.usable_energy * 50000 / CCAirUsed

    @property
    def economy(self):
        """(kJ/ccFuel) The energy potential of this reaction"""
        ccFuel = self.fuel_in * self.fuel.molarMass / self.fuel.density
        return self.usable_energy / ccFuel

    def _doCalcs(self):
        """Do calculations for this reaction"""
        self._simplifyReaction()
    
    def RichCombustion(fuel: Molecule):
        """A rich reaction, burning as much fuel as possible with the availble oxygen"""
        reaction = Reaction()
        reaction.fuel = fuel
        reaction.fuel_in = 4
        reaction.H2O_out = int(fuel.hydrogen * reaction.fuel_in / 2)
        reaction.CO_out = fuel.carbon * reaction.fuel_in
        reaction.O2_in = int(reaction.CO_out / 2 + reaction.H2O_out / 2 - fuel.oxygen * reaction.fuel_in / 2)
        reaction.CO2_out = 0
        reaction._doCalcs()
        return reaction

    def LeanCombustion(fuel: Molecule):
        """A lean combustion, reacting as much oxygen as possible with the fuel"""
        reaction = Reaction()
        reaction.fuel = fuel
        reaction.fuel_in = 4
        reaction.H2O_out = int(fuel.hydrogen * reaction.fuel_in / 2)
        reaction.CO2_out = fuel.carbon * reaction.fuel_in
        reaction.O2_in = int(reaction.CO2_out + reaction.H2O_out / 2 - fuel.oxygen * reaction.fuel_in / 2)
        reaction.CO_out = 0
        reaction._doCalcs()
        return reaction

    def __str__(self):
        """Define str(Reaction reaction)"""
        tmpStr = f"{self.fuel_in}{self.fuel.chemicalFormula} + {self.O2_in}O2 -> {self.H2O_out}H2O"
        if self.CO_out > 0 : 
            tmpStr += f" + {self.CO_out}CO"
        if self.CO2_out > 0 : 
            tmpStr += f" + {self.CO2_out}CO2"
        return tmpStr

if __name__ == "__main__":
    while(True):
        response = input("What is the name of this chemical? (respond L for a list of known chemicals)\n")
        response = response.lower()
        if response == "list" or response =="l" or response == "ls":
            Molecule.ListKnown()
            continue
        molecule = Molecule(name=response)
        if molecule.chemicalFormula == "":
            molecule = Molecule(formula=response)
        combustions = [Reaction.LeanCombustion(molecule), Reaction.RichCombustion(molecule)]
        leanAfr = combustions[0].airFuelRatio
        for combustion in combustions:
            afr = combustion.airFuelRatio
            print(str(combustion) + f"    At air:fuel ratio of {afr:.2f}")
            print(f"{combustion.power:.2f} kW from 1L engine at 6000RPM")
            print(f"{combustion.economy:.2f} kJ per cc of this fuel")
            print()