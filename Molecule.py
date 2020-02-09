class Molecule:
    """The smallest unit of a particular chemical"""
    
    def __init__(self, carbon = 0, hydrogen = 0, oxygen = 0, nitrogen = 0, density = None, formula = None, name = None):
        self._density = density
        import json
        def parse(jsonMolecule):
            if "formula" in jsonMolecule:
                self.chemicalFormula = jsonMolecule["formula"]
            if "density" in jsonMolecule:
                self._density = jsonMolecule["density"]
            if "enthalpy" in jsonMolecule:
                self._enthalpy = jsonMolecule["enthalpy"]
            if "entropy" in jsonMolecule:
                self._entropy = jsonMolecule["entropy"]
            if "specific_heat" in jsonMolecule:
                self._specificHeat = jsonMolecule["specific_heat"]
        if formula != None:
            formula = formula.upper()
            self.chemicalFormula = formula
            with open("knownMolecules.json") as json_file:
                knownMolecules = json.load(json_file)
                for molecule in knownMolecules:
                    _molecule = knownMolecules[molecule]
                    if _molecule["formula"] == formula:
                        parse(_molecule)
                        break
        elif name != None:
            import json
            with open("knownMolecules.json") as json_file:
                knownMolecules = json.load(json_file)
                if name in knownMolecules:
                    parse(knownMolecules[name])
                else:
                    print("WARNING: This molecule is not known by name in knownMolecules.json.\n" +
                        "Please add " + name + " to knownMolecules.json if you wish to use it by name.")
        else:
            self._carbon = carbon
            self._hydrogen = hydrogen
            self._oxygen = oxygen
            self._nitrogen = nitrogen
            self._density = density

    _carbon = 0
    @property
    def carbon(self):
        """The number of carbon atoms in this molecule"""
        return self._carbon
    
    _hydrogen = 0
    @property
    def hydrogen(self):
        """The number of hydrogen atoms in this molecule"""
        return self._hydrogen
    
    _oxygen = 0
    @property
    def oxygen(self):
        """The number of oxygen atoms in this molecule"""
        return self._oxygen

    _nitrogen = 0
    @property
    def nitrogen(self):
        """The number of oxygen atoms in this molecule"""
        return self._nitrogen
    
    _enthalpy = 0
    @property
    def enthalpy(self):
        """(kJ/mol) The enthalpy of formation for this molecule"""
        return self._enthalpy
    
    _entropy = 0
    @property
    def entropy(self):
        """(J/molK) The molar entropy of this molecule"""
        return self._entropy
    @entropy.setter
    def entropy(self, entropy):
        self._entropy = entropy
    
    _density = 0
    @property
    def density(self):
        """(g/cc) The density of fluid composed of this molecule at STP"""
        return self._density
    @density.setter
    def density(self, density):
        self._density = density

    _specificHeat = 1.
    @property
    def specificHeat(self):
        """(J/gK) The specific heat of this molecule"""
        return self._specificHeat
    @specificHeat.setter
    def specificHeat(self, specificHeat):
        self._specificHeat = specificHeat
    
    @property
    def molarMass(self):
        """(g/mol) The molar mass of this molecule"""
        return 12.0107 * self._carbon + 1.00794 * self._hydrogen + 15.999 * self._oxygen + 14.0067 * self._nitrogen

    @property
    def chemicalFormula(self):
        """The chemical formula for this molecule"""
        formula = ""
        if self._carbon > 0:
            formula += "C" + str(self._carbon)
        if self._hydrogen > 0:
            formula += "H" + str(self._hydrogen)
        if self._oxygen > 0:
            formula += "O" + str(self._oxygen)
        if self._nitrogen > 0:
            formula += "N" + str(self._nitrogen)
        return formula

    @chemicalFormula.setter
    def chemicalFormula(self, formula):
        """
        Set the formula of this molecule
        Will affect the number of each atom type
        """
        def getNumber(formula, index):
            """Gets the number of atoms of the type indicated by the index"""
            if index == len(formula) - 1:
                return 1
            index += 1
            if not formula[index].isnumeric():
                return 1
            tmpString = ""
            while (index < len(formula) and formula[index].isnumeric()):
                tmpString += formula[index]
                index += 1
            return int(tmpString)

        index = formula.upper().find('C')
        if index > -1:
            self._carbon = getNumber(formula, index)
        else: self._carbon = 0
        index = formula.upper().find('H')
        if index > -1:
            self._hydrogen = getNumber(formula, index)
        else: self._hydrogen = 0
        index = formula.upper().find('O')
        if index > -1:
            self._oxygen = getNumber(formula, index)
        else: self._oxygen = 0
        index = formula.upper().find('N')
        if index > -1:
            self._nitrogen = getNumber(formula, index)
        else: self._nitrogen = 0

    def ListKnown():
        """List all Molecules known by knownMolecules.json"""
        import json
        with open("knownMolecules.json") as knownMolecules:
            for molecule in json.load(knownMolecules):
                print(molecule)

    def __str__(self):
        return f"{self.chemicalFormula}, density: {self._density}, enthalpy: {self.enthalpy}, entropy: {self.entropy}"