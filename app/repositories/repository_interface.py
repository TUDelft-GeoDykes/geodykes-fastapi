'''
Repository Design Pattern: Simplifying Data Access
Below is the step-by-step explanation of the Repository Design Pattern

The Repository Design Pattern is a software design pattern that acts 
as an intermediary layer between an application’s business logic and data storage.
Its primary purpose is to provide a structured and standardized way to access, 
manage, and manipulate data while abstracting the underlying details of data storage technologies.
This pattern promotes a clear separation of concerns, making software more maintainable, testable, 
and adaptable to changes in data sources, without entangling the core application logic with data access intricacies.

In essence, the Repository Design Pattern is a blueprint for organizing and simplifying data access, 
enhancing the efficiency and flexibility of software systems.

We use it here also for development purposes to disconnect the development of the database
from the development of the application. This way, we can develop the application without
having to worry about the database implementation.
'''
from abc import ABC, abstractmethod
from typing import List
from app.apps.dykes.models import Reading

class ReadingRepository(ABC):
    @abstractmethod
    async def get_all_readings(self) -> List[Reading]:
        pass
