#include <omp.h>
#include <stdio.h>

int main() {
#pragma omp parallel
    {
        int nr_threads = 1;
        int thread_nr = 0;
#ifdef _OPENMP
        nr_threads = omp_get_num_threads();
        thread_nr = omp_get_thread_num();
#endif
        printf("hello from thread %d out of %d\n", thread_nr, nr_threads);
    }
    return 0;
}
