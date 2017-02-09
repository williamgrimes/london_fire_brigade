import pandas as pd
from datetime import datetime

class DataCleaning(object):
    """methods for cleaning lfb data"""

    def convert_date_time(df):
        """convert time to time stamp object"""
        df['DDDateTimeOfCall'] = df["DDDateTimeOfCall"].apply(lambda x: datetime.strptime(x,"%Y-%m-%d %H:%M:%S.%f"))
        return df

    def drop_columns(df):
        """remove columns that are noisy or do not provide useful information"""
        df = df.drop('IncidentType', 1)
        df = df.drop('FireInvestigationAttendanceID', 1)
        df = df.drop('LocationOfFirestartOther', 1)
        df = df.drop('OrganisationName', 1)
        df = df.drop('maincausemodel', 1)
        df = df.drop('maincauseappliancemanufacturerother', 1)
        return df

    def drop_rows(df):
        """remove rows that are not geolocated"""
        df = df[df['PropertyClass'].notnull()]
        df = df[df['PropertyCategory'].notnull()]
        df = df[df['ParentPropertyType'].notnull()]
        df = df[df['PropertyType'].notnull()]
        df = df[df['PostCode'].notnull()]
        df = df[df['IncGeo_BoroughCode'].notnull()]
        df = df[df['IncGeo_BoroughName'].notnull()]
        df = df[df['IncGeo_WardCode'].notnull()]
        df = df[df['IncGeo_WardName'].notnull()]
        return df

    def fill_missing_values(df):
        """handle rows with incomplete or missing values"""
        df['IgnitionToDiscovery'] = df['IgnitionToDiscovery'].fillna('Not known')
        df['DiscoveryToCall'] = df['DiscoveryToCall'].fillna('Not known')
        df['Action'] = df['Action'].fillna('Not known')
        df['ActionParent'] = df['ActionParent'].fillna('None')
        df['FloorOrDeckOfOrigin'] = df['FloorOrDeckOfOrigin'].fillna(0)
        df['TenureDescription'] = df['TenureDescription'].fillna('Not \
                                                                 applicable')
        df['PossibleMentalHealthIssues'] = df['PossibleMentalHealthIssues'].fillna(0)
        df['PossibleMobilityIssues'] = df['PossibleMobilityIssues'].fillna(0)
        df['EvidenceOfAlcoholConsumption'] = df['EvidenceOfAlcoholConsumption'].fillna(0)
        df['EvidenceOfPrescriptionDrugUse'] = df['EvidenceOfPrescriptionDrugUse'].fillna(0)
        df['EvidenceOfRecreationalDrugUse'] = df['EvidenceOfRecreationalDrugUse'].fillna(0)
        df['socialcarebeingreceived'] = df['socialcarebeingreceived'].fillna(0)
        df['OtherHumanFactor'] = df['OtherHumanFactor'].fillna('Not known')
        df['PropertyCoveredByRro'] = df['PropertyCoveredByRro'].fillna(0)
        df['NumPumps'] = df['NumPumps'].fillna(1)
        df['MainCause'] = df['MainCause'].fillna('Not applicable')
        df['ParentMainCause'] = df['ParentMainCause'].fillna('Motive: Not known')
        df['IgnitionSourcePower'] = df['IgnitionSourcePower'].fillna('Unknown')
        df['ParentIgnSource'] = df['ParentIgnSource'].fillna('Unknown')
        df['IgnitionSource'] = df['IgnitionSource'].fillna('Unknown')
        df['ItemFirstIgnited'] = df['ItemFirstIgnited'].fillna('Not known')
        df['ParentItemFirstIgnited'] = df['ParentItemFirstIgnited'].fillna('Other/Not known')
        df['LocationFireStarted'] = df['LocationFireStarted'].fillna('Not known')
        df['HouseholdOccupancy'] = df['HouseholdOccupancy'].fillna('Other')
        df['OccupationStatus'] = df['OccupationStatus'].fillna('Not known')
        df['CausedBy'] = df['CausedBy'].fillna('Not known')
        return df

    def all_cleaning(df):
        """perform all cleaning operations"""
        df = DataCleaning.convert_date_time(df)
        df = DataCleaning.drop_columns(df)
        df = DataCleaning.drop_rows(df)
        df = DataCleaning.fill_missing_values(df)
        return df
