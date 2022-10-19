cmake_minimum_required( VERSION 3.0 )

project (guidefield_measurement)

set(INCLUDES src/include )
include_directories(${INCLUDES})

add_executable( parser src/parser.cpp )
install( TARGETS parser 
		DESTINATION ${CMAKE_SOURCE_DIR}/execs )
