class House:
    def __init__(self, year, state, state_po, state_fips, state_cen,
                 state_ic, office, district, stage, runoff, special,
                 candidate, party, writein, mode, candidatevotes,
                 totalvotes, unofficial, version):
        self.__year = year
        self.__state = state
        self.__state_po = state_po
        self.__state_fips = state_fips
        self.__state_cen = state_cen
        self.__state_ic = state_ic
        self.__office = office
        self.__district = district
        self.__stage = stage
        self.__runoff = runoff
        self.__special = special
        self.__candidate = candidate
        self.__party = party
        self.__writein = writein
        self.__mode = mode
        self.__candidatevotes = candidatevotes
        self.__totalvotes = totalvotes
        self.__unofficial = unofficial
        self.__version = version

    # accessor
    def get_year(self):
        return self.__year

    def get_state(self):
        return self.__state

    def get_state_po(self):
        return self.__state_po

    def get_state_fips(self):
        return self.__state_fips

    def get_state_cen(self):
        return self.__state_cen

    def get_state_ic(self):
        return self.__state_ic

    def get_office(self):
        return self.__office

    def get_district(self):
        return self.__district

    def get_stage(self):
        return self.__stage

    def get_runoff(self):
        return self.__runoff

    def get_special(self):
        return self.__special

    def get_candidate(self):
        return self.__candidate

    def get_party(self):
        return self.__party

    def get_writein(self):
        return self.__writein

    def get_mode(self):
        return self.__mode

    def get_candidatevotes(self):
        return self.__candidatevotes

    def get_totalvotes(self):
        return self.__totalvotes

    def get_unofficial(self):
        return self.__unofficial

    def get_version(self):
        return self.__version

    # mutator

    def set_year(self, year):
        self.__year = year

    def set_state(self, state):
        self.__state = state

    def set_state_po(self, state_po):
        self.__state_po = state_po

    def set_state_fips(self, state_fips):
        self.__state_fips = state_fips

    def set_state_cen(self, state_cen):
        self.__state_cen = state_cen

    def set_state_ic(self, state_cen):
        self.__state_ic = state_cen

    def set_office(self, office):
        self.__office = office

    def set_district(self, district):
        self.__district = district

    def set_stage(self, stage):
        self.__stage = stage

    def set_runoff(self, runoff):
        self.__runoff = runoff

    def set_special(self, special):
        self.__special = special

    def set_candidate(self, candidate):
        self.__candidate = candidate

    def set_party(self, party):
        self.__party = party

    def set_writein(self, writein):
        self.__writein = writein

    def set_mode(self, mode):
        self.__mode = mode

    def set_candidatevotes(self, candidatevotes):
        self.__candidatevotes = candidatevotes

    def set_totalvotes(self, totalvotes):
        self.__totalvotes = totalvotes

    def set_unofficial(self, unofficial):
        self.__unofficial = unofficial

    def set_version(self, version):
        self.__version = version

    def __str__(self):
        return self.__year + ", " + \
               self.__state + ", " + \
               self.__state_po + ", " + \
               self.__state_fips + ", " + \
               self.__state_cen + ", " + \
               self.__state_ic + ", " + \
               self.__office + ", " + \
               self.__district + ", " + \
               self.__stage + ", " + \
               self.__runoff + ", " + \
               self.__special + ", " + \
               self.__candidate + ", " + \
               self.__party + ", " + \
               self.__writein + ", " + \
               self.__mode + ", " + \
               self.__candidatevotes + ", " + \
               self.__totalvotes + ", " + \
               self.__unofficial + ", " + \
               self.__version + ". "


class President:
    def __init__(self, year, state, state_po, state_fips, state_cen,
                 state_ic, office, candidate, party, writein, candidatevotes,
                 totalvotes, version, notes):
        self.__year = year
        self.__state = state
        self.__state_po = state_po
        self.__state_fips = state_fips
        self.__state_cen = state_cen
        self.__state_ic = state_ic
        self.__office = office
        self.__candidate = candidate
        self.__party = party
        self.__writein = writein
        self.__candidatevotes = candidatevotes
        self.__totalvotes = totalvotes
        self.__version = version
        self.__notes = notes

    # accessor
    def get_year(self):
        return self.__year

    def get_state(self):
        return self.__state

    def get_state_po(self):
        return self.__state_po

    def get_state_fips(self):
        return self.__state_fips

    def get_state_cen(self):
        return self.__state_cen

    def get_state_ic(self):
        return self.__state_ic

    def get_office(self):
        return self.__office

    def get_candidate(self):
        return self.__candidate

    def get_party(self):
        return self.__party

    def get_writein(self):
        return self.__writein

    def get_candidatevotes(self):
        return self.__candidatevotes

    def get_totalvotes(self):
        return self.__totalvotes

    def get_version(self):
        return self.__version

    def get_notes(self):
        return self.__notes

    # mutator

    def set_year(self, year):
        self.__year = year

    def set_state(self, state):
        self.__state = state

    def set_state_po(self, state_po):
        self.__state_po = state_po

    def set_state_fips(self, state_fips):
        self.__state_fips = state_fips

    def set_state_cen(self, state_cen):
        self.__state_cen = state_cen

    def set_state_ic(self, state_cen):
        self.__state_ic = state_cen

    def set_office(self, office):
        self.__office = office

    def set_candidate(self, candidate):
        self.__candidate = candidate

    def set_party(self, party):
        self.__party = party

    def set_writein(self, writein):
        self.__writein = writein

    def set_candidatevotes(self, candidatevotes):
        self.__candidatevotes = candidatevotes

    def set_totalvotes(self, totalvotes):
        self.__totalvotes = totalvotes

    def set_version(self, version):
        self.__version = version

    def set_notes(self, notes):
        self.__notes = notes

    def __str__(self):
        return self.__year + ", " + \
               self.__state + ", " + \
               self.__state_po + ", " + \
               self.__state_fips + ", " + \
               self.__state_cen + ", " + \
               self.__state_ic + ", " + \
               self.__office + ", " + \
               self.__candidate + ", " + \
               self.__party + ", " + \
               self.__writein + ", " + \
               self.__candidatevotes + ", " + \
               self.__totalvotes + ", " + \
               self.__version + ", " + \
               self.__notes + ". "
