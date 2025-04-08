// -*- c++ -*-

#include <cuComplex.h>
#include <cuda.h>
#include <cuda_fp16.h>
#include <cuda_runtime.h>
#include <stdexcept>
#include <stdio.h>

#ifndef BITREV_PERM
#define BITREV_PERM

#if defined(V1)
#define VSIZE 1
#elif defined(V2)
#define VSIZE 2
#elif defined(V3)
#define VSIZE 3
#elif defined(V4)
#define VSIZE 4
#endif

#ifdef USE_FLOAT16
#define SUPPORT_FLOAT16
#endif

#ifdef USE_FLOAT32
#define SUPPORT_FLOAT32
#endif

#ifdef USE_COMPLEX64
#define SUPPORT_COMPLEX64
#define SUPPORT_COMPLEX
#endif

#ifdef USE_FLOAT64
#define SUPPORT_FLOAT64
#endif

#ifdef USE_COMPLEX128
#define SUPPORT_COMPLEX128
#define SUPPORT_COMPLEX
#endif

#ifdef SUPPORT_FLOAT16
typedef __half dtype;
#if defined(V1)
typedef __half dtypex;
#endif
#if defined(V2)
typedef __half2 dtypex;
#endif
#if defined(V3)
typedef half3 dtypex;
#endif
#if defined(V4)
typedef half4 dtypex;
#endif
#endif

#ifdef SUPPORT_FLOAT32
typedef float dtype;
#if defined(V1)
typedef float dtypex;
#endif
#if defined(V2)
typedef float2 dtypex;
#endif
#if defined(V3)
typedef float3 dtypex;
#endif
#if defined(V4)
typedef float4 dtypex;
#endif
#endif

#ifdef SUPPORT_FLOAT64
typedef double dtype;
#if defined(V1)
typedef double dtypex;
#endif
#if defined(V2)
typedef double2 dtypex;
#endif
#if defined(V3)
typedef double3 dtypex;
#endif
#if defined(V4)
typedef double4 dtypex;
#endif
#endif

#ifdef SUPPORT_COMPLEX64
typedef cuFloatComplex dtype;
typedef float elt_t;
#if defined(V1)
typedef cuFloatComplex dtypex;
#endif
#if defined(V2)
typedef float4 dtypex;
#endif
#if defined(V3)
typedef float4 dtypex;
#endif
#if defined(V4)
typedef float4 dtypex;
#endif
#endif

#ifdef SUPPORT_COMPLEX128
typedef cuDoubleComplex dtype;
typedef double elt_t;
#if defined(V1)
typedef cuDoubleComplex dtypex;
#endif
#if defined(V2)
typedef double4 dtypex;
#endif
#if defined(V3)
typedef double4 dtypex;
#endif
#if defined(V4)
typedef double4 dtypex;
#endif
#endif

#define loadx(a, b)                                                            \
  reinterpret_cast<dtypex *>(&a)[0] = reinterpret_cast<dtypex *>(&b)[0]

#ifdef SUPPORT_COMPLEX
__device__ inline void make_cuXComplex(dtype &dst, elt_t r, elt_t i) {
#if defined(SUPPORT_COMPLEX64)
  dst = make_cuFloatComplex(r, i);
#else
  dst = make_cuDoubleComplex(r, i);
#endif
}
#endif

extern "C" {
__global__ void bitrev_perm(int *indices, dtype *input, dtype *output, int batch_size) {
  int ty = blockIdx.y * blockDim.y + threadIdx.y;
  int tx = threadIdx.x;
  int idx = indices[ty];
  dtypex src;
  for (int i = tx * (batch_size / blockDim.x); i < (tx + 1) * (batch_size / blockDim.x); i += VSIZE) {
#ifdef SUPPORT_COMPLEX
    // No cuFloatComplexX and cuDoubleComplexX structs yet ?
#if defined(V2)
    loadx(src, input[idx * batch_size + i]);
    make_cuXComplex(output[ty * batch_size + i + 0], src.x, src.y);
    make_cuXComplex(output[ty * batch_size + i + 1], src.z, src.w);
#else
#if defined(V3)
    loadx(src, input[idx * batch_size + i]);
    make_cuXComplex(output[ty * batch_size + i + 0], src.x, src.y);
    make_cuXComplex(output[ty * batch_size + i + 1], src.z, src.w);
    output[ty * batch_size + i + 2] = input[idx * batch_size + i + 2];
#else
#if defined(V4)
    loadx(src, input[idx * batch_size + i]);
    make_cuXComplex(output[ty * batch_size + i + 0], src.x, src.y);
    make_cuXComplex(output[ty * batch_size + i + 1], src.z, src.w);
    loadx(src, input[idx * batch_size + i + 2]);
    make_cuXComplex(output[ty * batch_size + i + 2], src.x, src.y);
    make_cuXComplex(output[ty * batch_size + i + 3], src.z, src.w);
#else
#pragma unroll
    for (int v = 0; v < VSIZE; v++)
      output[ty * batch_size + i + v] = input[idx * batch_size + i + v];
#endif
#endif
#endif
#else
#if defined(V1)
    output[ty * batch_size + i] = input[idx * batch_size + i];
#else
    loadx(output[ty * batch_size + i], input[idx * batch_size + i]);
#endif
#endif
  }
}
}

#endif
