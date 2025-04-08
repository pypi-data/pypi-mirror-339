"""
Advanced S3 Partitioned Data Loader

This module provides a high-performance interface for loading partitioned data from S3
with support for ticker and date-based partitioning schemes, parallel loading,
and comprehensive filtering capabilities.
"""

from typing import Dict, List, Optional, Union, Any, Tuple, Callable
import pyarrow.dataset as ds
import pyarrow as pa
import pandas as pd
import os
import datetime
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
from functools import lru_cache
from pyarrow.fs import S3FileSystem

# Try to import custom extensions when available
try:
    from sovai.extensions.pandas_extensions import CustomDataFrame
    HAS_CUSTOM_DATAFRAME = True
except ImportError:
    HAS_CUSTOM_DATAFRAME = False
    CustomDataFrame = pd.DataFrame

from sovai.tools.authentication import authentication

# =========================================================================
# Logging Configuration
# =========================================================================

logger = logging.getLogger(__name__)
if not logger.handlers:
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("data_operations.log"),
            logging.StreamHandler()
        ]
    )

# =========================================================================
# Filesystem Access
# =========================================================================

@lru_cache(maxsize=2)
def get_s3_filesystem(provider: str = "digitalocean") -> S3FileSystem:
    """
    Get cached S3 filesystem for the specified provider.
    
    Args:
        provider: Cloud provider identifier (default: "digitalocean")
        
    Returns:
        Authenticated S3FileSystem instance with caching
    """
    return authentication.get_s3_filesystem_pickle(provider, verbose=True)

# =========================================================================
# Path Management
# =========================================================================

class PathBuilder:
    """Utility class for building and managing S3 data paths."""
    
    @staticmethod
    def clean_path(path: str) -> str:
        """Remove s3:// prefix if present for consistent path handling."""
        return path.replace('s3://', '')
    
    @staticmethod
    def build_ticker_path(
        base_path: str, 
        ticker: str, 
        has_year: bool = True, 
        year: Optional[int] = None
    ) -> str:
        """
        Build a complete ticker-partitioned path.
        
        Args:
            base_path: Base S3 path to ticker partitions
            ticker: Ticker symbol
            has_year: Whether ticker partitions include year subdirectories
            year: Optional year for year-partitioned data
            
        Returns:
            Complete S3 path for the ticker partition
        """
        clean_path = PathBuilder.clean_path(base_path)
        ticker_path = f"{clean_path}/ticker_partitioned={ticker}"
        
        if has_year and year is not None:
            return f"{ticker_path}/year={year}/"
        return f"{ticker_path}/"

# =========================================================================
# Partition Discovery
# =========================================================================

class PartitionFinder:
    """Methods for discovering data partitions in the S3 storage."""
    
    @staticmethod
    def find_ticker_partitions(
        ticker_base_path: str, 
        tickers: List[str],
        has_year: bool = True,
        start_year: Optional[int] = None,
        end_year: Optional[int] = None
    ) -> List[Tuple[str, str]]:
        """
        Find all valid ticker partitions with optional year filtering.
        
        Args:
            ticker_base_path: Base path to ticker partitions
            tickers: List of tickers to search for
            has_year: Whether ticker partitions include year subdirectories
            start_year: Optional starting year to filter by
            end_year: Optional ending year to filter by
            
        Returns:
            List of tuples (path, ticker) for loading
        """
        fs = get_s3_filesystem()
        partitions = []
        
        # Process each ticker
        for ticker in tickers:
            ticker_path = f"{ticker_base_path}/ticker_partitioned={ticker}"
            
            try:
                # Case 1: No year partitioning
                if not has_year:
                    partitions.append((ticker_path, ticker))
                    continue
                    
                # Case 2: Year partitioning
                years = PartitionFinder._extract_years(
                    fs, ticker_path, start_year, end_year
                )
                    
                # Generate specific year paths
                for year in years:
                    year_path = f"{ticker_path}/year={year}"
                    partitions.append((year_path, ticker))
                    
                # If no years found but we know they exist, generate paths for requested years
                if not years and start_year and end_year:
                    for year in range(start_year, end_year + 1):
                        year_path = f"{ticker_path}/year={year}"
                        partitions.append((year_path, ticker))
                        
            except Exception as e:
                logger.error(f"Error processing ticker {ticker}: {e}")
        
        if not partitions:
            logger.warning(f"No ticker partitions found at {ticker_base_path} for tickers {tickers}")
            
        return partitions
    
    @staticmethod
    def _extract_years(
        fs: S3FileSystem, 
        ticker_path: str, 
        start_year: Optional[int], 
        end_year: Optional[int]
    ) -> List[int]:
        """
        Extract valid years from ticker subdirectories.
        
        Args:
            fs: S3 filesystem
            ticker_path: Path to search for year directories
            start_year: Optional starting year filter
            end_year: Optional ending year filter
            
        Returns:
            List of valid years within the specified range
        """
        years = []
        
        try:
            subdirs = fs.ls(ticker_path)
            for subdir in subdirs:
                basename = os.path.basename(subdir.rstrip('/'))
                if basename.startswith('year='):
                    year_str = basename.split('=')[1]
                    try:
                        year = int(year_str)
                        # Apply year filtering if needed
                        if ((start_year is None or year >= start_year) and
                            (end_year is None or year <= end_year)):
                            years.append(year)
                    except ValueError:
                        logger.warning(f"Invalid year format: {year_str}")
        except Exception as e:
            logger.warning(f"Error listing years: {e}")
            
        return years
            
    @staticmethod
    def find_date_partitions(
        date_base_path: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> List[str]:
        """
        Find all date partitions within the specified range.
        
        Args:
            date_base_path: Base path to date partitions
            start_date: Optional start date in YYYY-MM-DD format
            end_date: Optional end date in YYYY-MM-DD format. If not provided and start_date is provided,
                    defaults to today + 7 days to include recent and near-future data
            
        Returns:
            List of S3 paths for matching date partitions
        """
        fs = get_s3_filesystem()
        date_paths = []
        
        # Clean up S3 path for consistent handling
        clean_path = PathBuilder.clean_path(date_base_path)
        
        # Ensure we're looking at the correct date partitions path
        if not clean_path.endswith('/date'):
            clean_path = f"{clean_path}/date"
        
        logger.info(f"Searching for date partitions at path: {clean_path}")
            
        try:
            # Set default end_date if only start_date is provided (today + 7 days)
            if start_date and not end_date:
                future_date = datetime.datetime.now().date() + datetime.timedelta(days=7)
                end_date = future_date.strftime('%Y-%m-%d')
                logger.info(f"No end_date provided, using default end date: {end_date}")
            
            # Convert date strings to date objects for comparison
            start_date_obj = pd.to_datetime(start_date).date() if start_date else None
            end_date_obj = pd.to_datetime(end_date).date() if end_date else None
            
            if start_date:
                logger.info(f"Filtering by start date: {start_date}")
            if end_date:
                logger.info(f"Filtering by end date: {end_date}")
            
            # List and filter date partitions
            try:
                partitions = fs.ls(clean_path)
                logger.info(f"Found {len(partitions)} potential date partitions")
                
                for path in partitions:
                    basename = os.path.basename(path.rstrip('/'))
                    if basename.startswith('date_partitioned='):
                        try:
                            date_str = basename.split('=')[1]
                            date_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
                            
                            # Apply date filtering
                            if ((start_date_obj is None or date_obj >= start_date_obj) and
                                (end_date_obj is None or date_obj <= end_date_obj)):
                                date_paths.append(path)
                                logger.debug(f"Added date partition: {path}")
                        except ValueError:
                            logger.warning(f"Invalid date format in path: {basename}")
            except Exception as e:
                logger.error(f"Error listing partitions: {e}")
                
                # Fallback: if we can't list directories, try to construct paths directly for specific dates
                if start_date and end_date:
                    start_dt = pd.to_datetime(start_date)
                    end_dt = pd.to_datetime(end_date)
                    current_dt = start_dt
                    
                    # Generate a range of dates between start and end dates
                    while current_dt <= end_dt:
                        date_str = current_dt.strftime('%Y-%m-%d')
                        path = f"{clean_path}/date_partitioned={date_str}"
                        date_paths.append(path)
                        current_dt += pd.Timedelta(days=1)
                    
                    logger.info(f"Generated {len(date_paths)} fallback date paths")
                
        except Exception as e:
            logger.error(f"Error in date partition processing at {clean_path}: {e}")
        
        logger.info(f"Returning {len(date_paths)} date partitions")
        return date_paths

# =========================================================================
# Data Loading
# =========================================================================

class DataLoader:
    """Core data loading functionality with filtering and parallelism."""
    
    @staticmethod
    def load_partition(
        path: str,
        ticker_filter: Optional[List[str]] = None,
        columns: Optional[List[str]] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> pd.DataFrame:
        """
        Load and filter data from a single partition.
        
        Args:
            path: S3 path to the partition
            ticker_filter: Optional list of tickers to filter by
            columns: Optional list of columns to load
            start_date: Optional start date for filtering
            end_date: Optional end date for filtering
            
        Returns:
            Filtered pandas DataFrame
        """
        fs = get_s3_filesystem()
        
        try:
            # Create dataset
            dataset = ds.dataset(path, filesystem=fs, format='parquet')
            
            # Build filter expressions
            filters = DataLoader._build_date_filters(start_date, end_date)
            
            # Apply filters to dataset
            if filters:
                filter_expr = filters[0]
                for f in filters[1:]:
                    filter_expr = filter_expr & f
                dataset = dataset.filter(filter_expr)
            
            # Load data
            table = dataset.to_table(columns=columns, use_threads=True)
            df = table.to_pandas()
            
            # Apply ticker filter if needed
            if ticker_filter and 'ticker' in df.columns:
                df = df[df['ticker'].isin(ticker_filter)]
                
            return df
        except Exception as e:
            logger.error(f"Error loading data from {path}: {e}")
            return pd.DataFrame()
    
    @staticmethod
    def _build_date_filters(
        start_date: Optional[str], 
        end_date: Optional[str]
    ) -> List[ds.Expression]:
        """
        Build PyArrow date filter expressions.
        
        Args:
            start_date: Optional start date string
            end_date: Optional end date string
            
        Returns:
            List of PyArrow filter expressions
        """
        filters = []
        
        # Date filters
        if start_date:
            start_date_obj = pd.to_datetime(start_date).date()
            start_date_pa = pa.scalar(start_date_obj, type=pa.date32())
            filters.append(ds.field('date') >= start_date_pa)
            
        if end_date:
            end_date_obj = pd.to_datetime(end_date).date()
            end_date_pa = pa.scalar(end_date_obj, type=pa.date32())
            filters.append(ds.field('date') <= end_date_pa)
            
        return filters
    
    @staticmethod
    def load_data_parallel(
        tasks: List[Tuple],
        max_workers: int = 8
    ) -> List[pd.DataFrame]:
        """
        Process loading tasks in parallel with progress tracking.
        
        Args:
            tasks: List of (path, ticker_filter, columns, start_date, end_date) tuples
            max_workers: Maximum number of concurrent loading threads
            
        Returns:
            List of loaded DataFrames
        """
        results = []
        
        # Process tasks in parallel
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_task = {
                executor.submit(DataLoader.load_partition, path, ticker_filter, columns, start_date, end_date): path
                for path, ticker_filter, columns, start_date, end_date in tasks
            }
            
            for future in tqdm(as_completed(future_to_task), total=len(tasks), desc="Loading data"):
                try:
                    df = future.result()
                    if not df.empty:
                        results.append(df)
                except Exception as e:
                    path = future_to_task[future]
                    logger.error(f"Task failed for {path}: {e}")
                    
        return results

# =========================================================================
# Main Loading Interface
# =========================================================================

def load_data(
    ticker_path: str = '',
    date_path: str = '',
    has_year: bool = True,
    tickers: Optional[List[str]] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    columns: Optional[List[str]] = None,
    max_workers: int = 8,
    post_process: Optional[Callable[[pd.DataFrame], pd.DataFrame]] = None
) -> pd.DataFrame:
    """
    Load data from S3 using both ticker and date partitioning schemes.
    
    Args:
        ticker_path: Base path for ticker partitions
        date_path: Base path for date partitions
        has_year: Whether ticker partitions include year subdirectories
        tickers: Optional list of tickers to filter by
        start_date: Optional start date in YYYY-MM-DD format
        end_date: Optional end date in YYYY-MM-DD format. If not provided and start_date is provided,
                defaults to today + 7 days to include recent and near-future data
        columns: Optional list of columns to load
        max_workers: Maximum number of concurrent loading threads
        post_process: Optional function to apply to the final DataFrame
        
    Returns:
        Combined pandas DataFrame with the requested data
    """
    tasks = []
    
    # Set default end_date if only start_date is provided (today + 7 days)
    if start_date and not end_date:
        future_date = datetime.datetime.now().date() + datetime.timedelta(days=7)
        end_date = future_date.strftime('%Y-%m-%d')
        logger.info(f"No end_date provided, using default end date: {end_date}")
    
    # Log the parameters for debugging
    logger.info(f"Loading data with parameters: ticker_path={ticker_path}, date_path={date_path}, "
               f"tickers={tickers}, start_date={start_date}, end_date={end_date}")
    
    # Convert single ticker to list
    if tickers and isinstance(tickers, str):
        tickers = [tickers]
    
    # Determine date range for year partitioning
    start_year, end_year = _get_year_range(start_date, end_date)
    
    # Performance optimization strategy:
    # 1. Always prefer ticker-based partitioning when tickers are provided (faster & more efficient)
    # 2. Only use date partitions when no tickers are provided OR no ticker path exists
    # 3. Apply date filtering after ticker-based loading
    
    use_ticker_partitions = tickers and ticker_path
    use_date_partitions = date_path and (not use_ticker_partitions)
    
    # Get ticker partitions if tickers provided and ticker_path exists
    if use_ticker_partitions:
        logger.info(f"Strategy: Using ticker partitions with date filtering (preferred for performance)")
        logger.info(f"Getting ticker partitions from {ticker_path}")
        ticker_partitions = PartitionFinder.find_ticker_partitions(
            ticker_path, 
            tickers,
            has_year,
            start_year,
            end_year
        )
        
        # Add ticker-specific loading tasks
        for path, ticker in ticker_partitions:
            tasks.append((path, [ticker], columns, start_date, end_date))
        
        logger.info(f"Added {len(ticker_partitions)} ticker-based loading tasks")
    
    # Only use date partitions if we're not using ticker partitions
    # This avoids loading the same data twice and prioritizes the more efficient ticker-based approach
    elif use_date_partitions:
        logger.info(f"Strategy: Using date partitions (fallback when no tickers provided)")
        logger.info(f"Getting date partitions from {date_path}")
        date_partitions = PartitionFinder.find_date_partitions(date_path, start_date, end_date)
        
        # Add date-based loading tasks - for date-only queries, we pass None for ticker_filter 
        # to ensure we get all tickers for the specified date range
        for path in date_partitions:
            tasks.append((path, None, columns, start_date, end_date))
        
        logger.info(f"Added {len(date_partitions)} date-based loading tasks")
    
    # If no tasks to process, return empty DataFrame
    if not tasks:
        logger.warning("No tasks generated. Check paths and parameters.")
        logger.info(f"Config details - ticker_path exists: {bool(ticker_path)}, date_path exists: {bool(date_path)}")
        if ticker_path:
            logger.info(f"Ticker path: {ticker_path}")
        if date_path:
            logger.info(f"Date path: {date_path}")
        return pd.DataFrame()
    
    # Process tasks in parallel
    results = DataLoader.load_data_parallel(tasks, max_workers)
    
    # Combine results
    if results:
        final_df = pd.concat(results, ignore_index=True)
        
        # Sort by ticker and date if available
        sort_cols = [col for col in ['ticker', 'date'] if col in final_df.columns]
        if sort_cols:
            final_df = final_df.sort_values(sort_cols)
            
        # Apply optional post-processing
        if post_process and callable(post_process):
            final_df = post_process(final_df)
        
        logger.info(f"Successfully loaded {len(final_df)} records")
        return final_df
    else:
        logger.warning("No data loaded from any partition")
        return pd.DataFrame()

def _get_year_range(
    start_date: Optional[str], 
    end_date: Optional[str]
) -> Tuple[Optional[int], Optional[int]]:
    """
    Determine year range from date strings.
    
    Args:
        start_date: Optional start date string
        end_date: Optional end date string. If not provided and start_date is provided,
                defaults to current year
        
    Returns:
        (start_year, end_year) tuple
    """
    start_year = None
    end_year = None
    
    if start_date:
        start_year = pd.to_datetime(start_date).year
    
    if end_date:
        end_year = pd.to_datetime(end_date).year
    elif start_year:
        # Default to current year + 1 if no end date (to include all current year data)
        end_year = datetime.datetime.now().year + 1
        logger.info(f"Using default end year: {end_year} (current year + 1)")
        
    return start_year, end_year

# =========================================================================
# Endpoint Configuration
# =========================================================================


# Updated endpoint configuration with all available directories
ENDPOINT_CONFIG = {
    "patents/applications": {
        "ticker_path": "sovai/sovai-patents-bulk/applications/ticker/ticker",
        "date_path": "sovai/sovai-patents-bulk/applications/date",
        "has_year": True
    },
    "patents/grants": {
        "ticker_path": "sovai/sovai-patents-bulk/grants/ticker/ticker",
        "date_path": "sovai/sovai-patents-bulk/grants/date",
        "has_year": True
    },
    "clinical/trials": {
        "ticker_path": "sovai/sovai-clinical-trials-export/partitioned/ticker/ticker",
        "date_path": "sovai/sovai-clinical-trials-export/partitioned/date/date",
        "has_year": False
    },
    "spending/awards": {
        "ticker_path": "sovai/sovai-government/partitioned/awards/ticker",
        "date_path": "sovai/sovai-government/partitioned/awards/date",
        "has_year": False
    },
    "spending/compensation": {
        "ticker_path": "sovai/sovai-government/partitioned/compensation/ticker",
        "date_path": "sovai/sovai-government/partitioned/compensation/date",
        "has_year": False
    },
    "spending/competition": {
        "ticker_path": "sovai/sovai-government/partitioned/competition/ticker",
        "date_path": "sovai/sovai-government/partitioned/competition/date",
        "has_year": False
    },
    "spending/contracts": {
        "ticker_path": "sovai/sovai-government/partitioned/contract/ticker",
        "date_path": "sovai/sovai-government/partitioned/contract/date",
        "has_year": False
    },
    "spending/product": {
        "ticker_path": "sovai/sovai-government/partitioned/product/ticker",
        "date_path": "sovai/sovai-government/partitioned/product/date",
        "has_year": False
    },
    "spending/transactions": {
        "ticker_path": "sovai/sovai-government/partitioned/transactions/ticker",
        "date_path": "sovai/sovai-government/partitioned/transactions/date",
        "has_year": False
    },
    "spending/entities": {
        "ticker_path": "sovai/sovai-government/partitioned/entities/ticker",
        "has_year": False
    },
    "spending/location": {
        "ticker_path": "sovai/sovai-government/partitioned/location/ticker",
        "has_year": False
    },
    "lobbying": {
        "ticker_path": "sovai/sovai-lobbying/partitioned/ticker",
        "date_path": "sovai/sovai-lobbying/partitioned/date",
        "has_year": False
    },
    "accounting/weekly": {
        "ticker_path": "sovai/sovai-accounting/partitioned/ticker",
        "date_path": "sovai/sovai-accounting/partitioned/date",
        "has_year": False
    },
    "ratios/normal": {
        "ticker_path": "sovai/sovai-ratios/partitioned/ticker",
        "date_path": "sovai/sovai-ratios/partitioned/date",
        "has_year": False
    },
    "complaints/public": {
        "ticker_path": "sovai/sovai-complaints/partitioned/ticker",
        "date_path": "sovai/sovai-complaints/partitioned/date",
        "has_year": False
    },
    "factors/accounting": {
        "ticker_path": "sovai/sovai-factors/accounting/partitioned/ticker",
        "date_path": "sovai/sovai-factors/accounting/partitioned/date",
        "has_year": False
    },
    "factors/alternative": {
        "ticker_path": "sovai/sovai-factors/alternative/partitioned/ticker",
        "date_path": "sovai/sovai-factors/alternative/partitioned/date",
        "has_year": False
    },
    "factors/comprehensive": {
        "ticker_path": "sovai/sovai-factors/comprehensive/partitioned/ticker",
        "date_path": "sovai/sovai-factors/comprehensive/partitioned/date",
        "has_year": False
    },
    "factors/coefficients": {
        "ticker_path": "sovai/sovai-factors/coefficients/partitioned/ticker",
        "date_path": "sovai/sovai-factors/coefficients/partitioned/date",
        "has_year": False
    },
    "factors/standard_errors": {
        "ticker_path": "sovai/sovai-factors/standard_errors/partitioned/ticker",
        "date_path": "sovai/sovai-factorss/standard_errors/partitioned/date",
        "has_year": False
    },
    "factors/t_statistics": {
        "ticker_path": "sovai/sovai-factors/t_statistics/partitioned/ticker",
        "date_path": "sovai/sovai-factors/t_statistics/partitioned/date",
        "has_year": False
    },
    "factors/model_metrics": {
        "ticker_path": "sovai/sovai-factors/model_metrics/partitioned/ticker",
        "date_path": "sovai/sovai-factors/model_metrics/partitioned/date",
        "has_year": False
    },
    "breakout": {
        "ticker_path": "sovai/sovai-breakout-price/partitioned/ticker",
        "date_path": "sovai/sovai-breakout-price/partitioned/date",
        "has_year": False
    },
    "visas/h1b": {
        "ticker_path": "sovai/sovai-employment/partitioned/ticker",
        "date_path": "sovai/sovai-employment/partitioned/date",
        "has_year": False
    }
}


# =========================================================================
# Public Interface
# =========================================================================

def load_frame_s3_partitioned_high(
    endpoint: str,
    tickers: Optional[Union[str, List[str]]] = None,
    columns: Optional[List[str]] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    post_process: Optional[Callable[[pd.DataFrame], pd.DataFrame]] = None
) -> pd.DataFrame:
    """
    Load data for the specified endpoint with ticker and date filtering.
    
    Args:
        endpoint: Name of the data endpoint (e.g., "clinical_trials")
        tickers: Optional ticker or list of tickers to filter by
        columns: Optional list of columns to load
        start_date: Optional start date in YYYY-MM-DD format
        end_date: Optional end date in YYYY-MM-DD format. If not provided and start_date is provided,
                defaults to today + 7 days to include recent and near-future data
        post_process: Optional function to apply to the final DataFrame
        
    Returns:
        DataFrame with the requested data
        
    Raises:
        ValueError: If endpoint is not configured
        
    Examples:
        >>> df = load_frame_s3_partitioned_high(
        ...     "clinical_trials", 
        ...     tickers=["AMGN", "PFE"],
        ...     start_date="2020-01-01",
        ...     end_date="2020-12-31"
        ... )
        
        >>> # Date-only query (from January 1, 2023 to today + 7 days)
        >>> df = load_frame_s3_partitioned_high(
        ...     "spending/awards",
        ...     start_date="2023-01-01"
        ... )
        
        >>> # Date-only query with explicit end date
        >>> df = load_frame_s3_partitioned_high(
        ...     "spending/awards",
        ...     start_date="2023-01-01",
        ...     end_date="2023-12-31"
        ... )
    """
    if endpoint not in ENDPOINT_CONFIG:
        raise ValueError(f"Invalid endpoint: {endpoint}. Available endpoints: {', '.join(ENDPOINT_CONFIG.keys())}")
    
    config = ENDPOINT_CONFIG[endpoint]
    
    # Log request info
    logger.info(f"Processing request for endpoint: {endpoint}")
    logger.info(f"Parameters: tickers={tickers}, start_date={start_date}, end_date={end_date}")
    
    # Get the appropriate paths for this endpoint
    ticker_path = config.get("ticker_path", "")
    date_path = config.get("date_path", "")
    
    # Determine query type for logging
    if tickers and (start_date or end_date):
        logger.info(f"Query type: Ticker + Date - Will prioritize ticker partitions for performance")
    elif tickers:
        logger.info(f"Query type: Ticker-only")
    elif start_date or end_date:
        logger.info(f"Query type: Date-only")
    
    # Validate that we have sufficient paths for the requested query type
    if tickers is None and not date_path:
        logger.warning(f"Date-based queries requested but endpoint {endpoint} doesn't support date partitioning")
        return pd.DataFrame()
    
    # Get appropriate paths, accounting for missing keys in some endpoints
    df = load_data(
        ticker_path=config.get("ticker_path", ""),
        date_path=config.get("date_path", ""),
        has_year=config.get("has_year", False),
        tickers=tickers,
        start_date=start_date,
        end_date=end_date,
        columns=columns,
        max_workers=8,
        post_process=post_process
    )
    
    # Convert to CustomDataFrame if available
    if HAS_CUSTOM_DATAFRAME:
        return CustomDataFrame(df)
    return df
