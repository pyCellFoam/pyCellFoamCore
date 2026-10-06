# About

pyCellFoam is a python library that implements the Cell Method  to simulate heat transfer on open cell foams. It was brought to life by the Munich node of the [INFIDHEM project](https://www.mw.tum.de/rt/emc/interconnected-systems-infidhem/) at the TUM Chair of Automatic Control in cooperation with LAGEPP at Université Claude Bernard Lyon 1. An example geometry that can be used in the cell method is shown in Fig. 1.

![Kelvin Cell](img/kelvin.png)
*Fig. 1: Cell complex based on a Kelvin Cell*

# Installation

## Python

This library is based on Python 3.8.

An installation of the python distribution [Anaconda](https://anaconda.org/) is recommended.

## Python packages

Hint: open anaconda prompt  with admin privileges.

* tabulate: `conda install -c conda-forge tabulate`
* sphinx: `conda install -c anaconda sphinx`
* fulltoc: `conda install -c conda-forge sphinxcontrib-fulltoc`
* automodule: `conda install -c conda-forge sphinx-autodoc-typehints`
* ffmpeg : `conda install -c conda-forge ffmpeg`
* (vtk?)

## Sphinx and library environment variable

Sphinx and this library need to be added to the environment variables:

1. Open environment variables
2. Open variable `Path` (If it does not exist yet, create it)
3. Add the folder where sphinx has been installed, it should be something like `C:\ProgramData\Anaconda3\Scripts`
4. Add the variable `PYTHONPATH`  to the environment variables. Set its value to the location where you cloned this repository.
5. Restart your computer so that the environment variables get updated.

# Tutorial

# Related Publications

# UML

```mermaid
classDiagram

    class SuperBaseCell{
        <<slots>>
    }

    class SuperCell {
        
    }

    class SuperReversedCell{
    }

    class BaseCell {
    }

    class Cell{
        <<slots>>
    }

    class ReversedCell{
    
    }

    class DualCell{
    
    }

    class BaseSimpleCell{
    
    }

    class SimpleCell{
    
    }

    class ReversedSimpleCell{
    
    }

    class Node{
        <<slots>>
    }

    class DualNode0D{
    
    }

    class DualNode1D{
    
    }

    class DualNode2D{
    
    }

    class DualNode3D{
    
    }

    class BaseEdge{
    
    }

    class Edge{
        <<slots>>
    }

    class ReversedEdge{
    
    }

    class DualEdge1D{
    
    }

    class DualEdge2D{
    
    }

    class DualEdge3D{
    
    }

    class BaseSimpleEdge{
    
    }    
    
    class SimpleEdge{
    
    }

    class ReversedSimpleEdge{
        
    }
    

    SuperBaseCell <|-- SuperCell
    SuperBaseCell <|-- BaseCell
    SuperBaseCell <|-- SuperReversedCell
    SuperBaseCell <|-- BaseSimpleCell
    BaseCell <|-- Cell
    BaseCell <|-- ReversedCell 
    BaseCell <|-- BaseEdge
    SuperCell <|-- Cell
    SuperCell <|-- SimpleCell
    SuperReversedCell <|-- ReversedCell
    SuperReversedCell <|-- ReversedSimpleCell
    Cell <|-- DualCell
    Cell <|-- Node
    Cell <|-- Edge
    ReversedCell <|-- ReversedEdge
    DualCell <|-- DualNode0D
    DualCell <|-- DualNode1D
    DualCell <|-- DualNode2D
    DualCell <|-- DualNode3D
    DualCell <|-- DualEdge1D
    DualCell <|-- DualEdge2D
    DualCell <|-- DualEdge3D
    BaseSimpleCell <|-- SimpleCell
    BaseSimpleCell <|-- ReversedSimpleCell
    BaseSimpleCell <|-- BaseSimpleEdge
    SimpleCell <|-- SimpleEdge
    ReversedSimpleCell <|-- ReversedSimpleEdge
    Node <|-- DualNode0D
    Node <|-- DualNode1D
    Node <|-- DualNode2D
    Node <|-- DualNode3D
    BaseEdge <|-- Edge
    BaseEdge <|-- ReversedEdge
    Edge <|-- DualEdge1D
    Edge <|-- DualEdge2D
    Edge <|-- DualEdge3D
    BaseSimpleEdge <|-- SimpleEdge
    BaseSimpleEdge <|-- ReversedSimpleEdge
    

```

```mermaid
classDiagram
    class Animal:::someclass
    classDef someclass fill:#f96
```
