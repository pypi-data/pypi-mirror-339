
#ifndef EXPORT_SWMM_SOLVER_API_H
#define EXPORT_SWMM_SOLVER_API_H

#ifdef SHARED_EXPORTS_BUILT_AS_STATIC
#  define EXPORT_SWMM_SOLVER_API
#  define SWMM5_NO_EXPORT
#else
#  ifndef EXPORT_SWMM_SOLVER_API
#    ifdef swmm5_EXPORTS
        /* We are building this library */
#      define EXPORT_SWMM_SOLVER_API __attribute__((visibility("default")))
#    else
        /* We are using this library */
#      define EXPORT_SWMM_SOLVER_API __attribute__((visibility("default")))
#    endif
#  endif

#  ifndef SWMM5_NO_EXPORT
#    define SWMM5_NO_EXPORT __attribute__((visibility("hidden")))
#  endif
#endif

#ifndef SWMM5_DEPRECATED
#  define SWMM5_DEPRECATED __attribute__ ((__deprecated__))
#endif

#ifndef SWMM5_DEPRECATED_EXPORT
#  define SWMM5_DEPRECATED_EXPORT EXPORT_SWMM_SOLVER_API SWMM5_DEPRECATED
#endif

#ifndef SWMM5_DEPRECATED_NO_EXPORT
#  define SWMM5_DEPRECATED_NO_EXPORT SWMM5_NO_EXPORT SWMM5_DEPRECATED
#endif

/* NOLINTNEXTLINE(readability-avoid-unconditional-preprocessor-if) */
#if 0 /* DEFINE_NO_DEPRECATED */
#  ifndef SWMM5_NO_DEPRECATED
#    define SWMM5_NO_DEPRECATED
#  endif
#endif

#endif /* EXPORT_SWMM_SOLVER_API_H */
