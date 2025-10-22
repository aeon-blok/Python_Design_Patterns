import asyncio
from abc import ABC, abstractmethod
from typing import List, Any
import random


# subject interface
class AsyncSubject(ABC):

    @abstractmethod
    async def attach(self, observer: "AsyncObserver") -> None:
        pass

    @abstractmethod
    async def detach(self, observer: "AsyncObserver") -> None:
        pass

    @abstractmethod
    async def _notify(self) -> None:
        pass

    @abstractmethod
    async def set_state(self, state) -> None:
        pass


# concrete subject
class ConcreteAsyncSubjectA(AsyncSubject):

    def __init__(self, name: str) -> None:
        self._observers: List[AsyncObserver] = []
        self._state = None
        self._name = name

    @property
    def state(self):
        return self._state

    @property
    def name(self):
        return self._name
    
    async def attach(self, observer: "AsyncObserver") -> None:
        if observer not in self._observers:
            self._observers.append(observer)    

    async def detach(self, observer: "AsyncObserver") -> None:
        if observer in self._observers:
            self._observers.remove(observer)

    async def _notify(self) -> None:
        # * operator unpacks the generator into separate positional arguments for asyncio.gather
        # return_exceptions=True -- catch exceptions instead of stopping
        results = await asyncio.gather(*(observer.update(self) for observer in self._observers), return_exceptions=True)

        # basic async error handling
        for item, result in enumerate(results):
            if isinstance(result, Exception):
                print(f"Error: Observer {self._observers[item]} failed: {result}")

    async def set_state(self, state) -> None:
        self._state = state
        await self._notify()


# observer interface
class AsyncObserver(ABC):

    @abstractmethod
    async def update(self, subject: AsyncSubject) -> None:
        pass


# concrete observer
class ConcreteAsyncObserver(AsyncObserver):
    def __init__(self, name: str) -> None:
        self._name = name

    async def update(self, subject: AsyncSubject) -> None:
        await asyncio.sleep(random.uniform(0.1,2))  # simulate async work
        print(f"{subject.name} Notified {self._name}: State Changes to: {subject.state}") # type: ignore


# Main -- Code Usage --

async def main():
    # initiailize Subjects
    subject_a = ConcreteAsyncSubjectA("Subject 1")
    subject_b = ConcreteAsyncSubjectA("Subject 2")

    # initialize Observers
    observer_a = ConcreteAsyncObserver("Async Observer A")
    observer_b = ConcreteAsyncObserver("Async Observer B")
    observer_c = ConcreteAsyncObserver("Async Observer C")
    observer_d = ConcreteAsyncObserver("Async Observer D")

    # Attach Observers to subject a
    await subject_a.attach(observer_a)
    await subject_a.attach(observer_b)
    # Attach Observers to subject b
    await subject_b.attach(observer_c)
    await subject_b.attach(observer_d)

    # change State
    await subject_a.set_state("Confabulatin....")
    await subject_b.set_state("Confabulatin....")

    # change State
    await subject_a.set_state("Target Acquired....")
    await subject_b.set_state("Target Acquired....")

    # change State
    await subject_a.set_state("Executing Payload....")
    await subject_b.set_state("Executing Payload....")

if __name__ == "__main__":
    asyncio.run(main())
