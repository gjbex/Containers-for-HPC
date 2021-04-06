cmake_minimum_required(VERSION 3.9)

project(mpi LANGUAGES Fortran)

set(CMAKE_Fortran_MODULE_DIRECTORY
    ${CMAKE_BINARY_DIR}/modules)
file(MAKE_DIRECTORY ${CMAKE_Fortran_MODULE_DIRECTORY})

add_compile_options(-Wall -Wextra)

find_package(MPI REQUIRED)
add_executable(hello.exe hello_world_f08.f90)
target_link_libraries(hello.exe PUBLIC MPI::MPI_Fortran)
