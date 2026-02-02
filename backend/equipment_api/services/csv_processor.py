import pandas as pd
from io import StringIO


class CSVProcessor:
    """Handles CSV file validation and parsing"""
    
    REQUIRED_COLUMNS = ['Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temperature']
    
    def validate_and_parse(self, csv_file):
        """
        Read CSV and check if all required columns exist
        Returns: pandas DataFrame or raises ValueError
        """
        try:
            # read csv file
            content = csv_file.read().decode('utf-8')
            df = pd.read_csv(StringIO(content))
            
            # check for required columns
            missing_cols = [col for col in self.REQUIRED_COLUMNS if col not in df.columns]
            if missing_cols:
                raise ValueError(f"Missing required columns: {', '.join(missing_cols)}")
            
            # basic data validation
            if df.empty:
                raise ValueError("CSV file is empty")
            
            # check numeric columns
            numeric_cols = ['Flowrate', 'Pressure', 'Temperature']
            for col in numeric_cols:
                if not pd.api.types.is_numeric_dtype(df[col]):
                    try:
                        df[col] = pd.to_numeric(df[col])
                    except:
                        raise ValueError(f"Column {col} must contain numeric values")
            
            return df
            
        except pd.errors.EmptyDataError:
            raise ValueError("CSV file is empty or invalid")
        except Exception as e:
            raise ValueError(f"Error processing CSV: {str(e)}")
