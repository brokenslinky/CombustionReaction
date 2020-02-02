from Molecule import Molecule

class Reaction:
    fuel: Molecule
    O2 = Molecule(formula="O2")
    H2O = Molecule(formula="H2O")
    CO = Molecule(formula="CO")
    CO2 = Molecule(formula="CO2")

    fuel_in = 0
    O2_in = 0
    H2O_out = 0
    CO_out = 0
    CO2_out = 0

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
        airDensity = 0.001225
        volumeRatioOfO2InAir = 0.209
        O2 = Reaction.O2
        massRatioOfO2InAir = volumeRatioOfO2InAir * O2.density / airDensity
        massOfAirReacted = self.O2_in * O2.molarMass / massRatioOfO2InAir
        massOfFuelReacted = self.fuel_in * self.fuel.molarMass
        return massOfAirReacted / massOfFuelReacted
    
    @property
    def enthalpy_out(self):
        """(kJ/mol) The change in enthalpy from this reaction"""
        return self.H2O_out * Reaction.H2O.enthalpy + self.CO2_out * Reaction.CO2.enthalpy + \
            self.CO_out * Reaction.CO.enthalpy - (
            self.fuel_in * self.fuel.enthalpy + self.O2_in * Reaction.O2.enthalpy)

    @property
    def entropy_out(self):
        """(J/molK) The change in entropy from this reaction"""
        return self.H2O_out * Reaction.H2O.entropy + self.CO2_out * Reaction.CO2.entropy + \
            self.CO_out * Reaction.CO.entropy - (
            self.fuel_in * self.fuel.entropy + self.O2_in * Reaction.O2.entropy)

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
            print(str(combustion) + f"    At an air:fuel ratio of {afr:.2f} ({afr / leanAfr:.2f} lambda)")
            print(f"{combustion.enthalpy_out} kJ/mol enthalpy change   {combustion.entropy_out} J/molK entropy change")