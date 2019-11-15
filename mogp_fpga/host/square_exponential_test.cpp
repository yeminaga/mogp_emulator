#define CL_HPP_ENABLE_EXCEPTIONS
#define CL_HPP_TARGET_OPENCL_VERSION 200

#include "CL/cl2.hpp"
#include <iostream>
#include <vector>

int main(){
    try{
        // Create context using default device
        cl::Context context(CL_DEVICE_TYPE_DEFAULT);
        // Create queue
        cl::CommandQueue queue(context);

        // Get devices
        std::vector<cl::Device> devices;
        context.getInfo(CL_CONTEXT_DEVICES, &devices);

        // Create queue from binary
        const char* binary_file_name = "square_exponential.aocx";
        FILE* fp;
        fp = fopen(binary_file_name, "rb");
        if(fp == 0) {
            throw cl::Error(0, "can't open aocx file");
        }
        // Get size of binary
        fseek(fp, 0, SEEK_END);
        size_t binary_size = ftell(fp);
        // Read binary as void*
        std::vector<unsigned char> binary(binary_size);
        rewind(fp);
        if (fread(&(binary[0]), binary_size, 1, fp) == 0) {
            fclose(fp);
            throw cl::Error(0, "error while reading kernel binary");
        }
        cl::Program::Binaries binaries(1, binary);

        // Create program
        cl::Program program(context, devices, binaries);
        // Create kernel functor
        auto square_exponential = cl::KernelFunctor<cl::Buffer, cl::Buffer, int, int>(program, "sq_exp");

        // Create host variables
        std::vector<float> h_r = {1.0, 2.0, 4.0, 8.0};
        std::vector<float> h_k(4, 0.0);
        int m=2, n=2;
        // Create device objects
        cl::Buffer d_r(h_r.begin(), h_r.end(), true);
        cl::Buffer d_k(h_k.begin(), h_k.end(), false);

        for (auto const& i : h_r)
            std::cout << i << ' ';

        // Call kernel
        square_exponential(cl::EnqueueArgs(queue, cl::NDRange(1)), d_r, d_k, m, n);

        queue.finish();

        cl::copy(d_k, h_k.begin(), h_k.end());

        for (auto const& i : h_k)
            std::cout << i << ' ';
    }
    catch (cl::Error err){
        std::cout << "OpenCL Error: " << err.what() << " code " << err.err() << std::endl;
        exit(-1);
    }

    return 0;
}
