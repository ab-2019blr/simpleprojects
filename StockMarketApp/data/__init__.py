# Package for StockMarketApp data handling
# This package contains modules for data collection, processing, and storage
# for the StockMarketApp project.

from .database import read_data, read_specific_data # Import read_data function from database module

__all__ = ['read_data', 'read_specific_data']  # Define the public interface of the package