# Change Log
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

## [0.2.1] - 2017-03-16

### Fixed
- Convert all terminal values to float type in ADD class

## [0.2.0] - 2017-03-16

### Added
- ADD class with factory methods for constructing terminals and variables
- ADD operator overloading for basic arithmetic manipulation (+, -, *, /)
- ADD unary minus (-) and unary negation (~) for variables
- ADD variable marginalization
- ADD string representation for debug

## [0.1.0] - 2017-03-09

### Added
- DD class implementing iterator over the structure of the the diagram
- DD operations reduce, apply and restrict
- BDD class with factory methods for constructing terminals and variables
- BDD operator overloading for basic boolean manipulation (AND, OR, NOT, XOR)
- BDD string representation for debug
