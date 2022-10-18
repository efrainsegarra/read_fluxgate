#include <iostream>
#include <fstream>
#include <vector>
#include <map>
#include <numeric>

#include "constants.h"

using namespace std;

double average(std::vector<double> const & v ){
	return std::accumulate( v.begin(), v.end() ,0.) / v.size();
}


struct Measure {
	double pos 	= DEFAULT;	// position of fluxgate [cm]
	double ang 	= DEFAULT;	// angular position of fluxgate [deg.]
	double Bx 	= DEFAULT;	// avg of magnetic field in x [pT]
	double By 	= DEFAULT;	// avg of magnetic field in y [pT]
	double Bz 	= DEFAULT;	// avg of magnetic field in z [pT]
	double eBx 	= DEFAULT;	// std of magnetic field in x [pT]
	double eBy 	= DEFAULT;	// std of magnetic field in y [pT]
	double eBz 	= DEFAULT;	// std of magnetic field in z [pT]
};

int main( int argc, char** argv ){

	ifstream file ("test.bin", ios::binary);

	/////////////////////////////////////////////////
	// File structure in binary:
	// 	each measurement is a series of 8 double-
	// 	precision numbers, 1 for each readout
	// 	channel
	// 	
	std::map<int,std::vector<double>> full_data;
	int channel = 0;
	for (double read = -1e5; file.read(reinterpret_cast<char*>(&read), sizeof(read)); ){

		// For some reason Georg has factors: 2*5 in front of channel 0, 
		// 2*7 in front of channel 1, and 7000 in front of 2-7 ...
		// ¯\_(ツ)_/¯
		full_data[channel].push_back( SCALING[channel] * read );

		// Reset after 8 channels read
		if( channel == MAXCHANNEL ){
			channel = 0;
			continue;
		}
		channel++;
	}
	if( full_data[0].size() != EXPECTEDSIZE ){ cerr << "Unexpected measurement size! Exiting...\n"; return -1; }
	
	/////////////////////////////////////////////////
	// Typically we only care about average reading 
	// per channel per angle per position:
	//
	Measure measure;
	measure.Bx 	= average(full_data[2]);
	measure.By 	= average(full_data[3]);
	measure.Bz 	= average(full_data[4]);



	// TODO:
	// - take sample measurement
	// - check how individual samples look like -- gaussian, some weird shape, etc..
	// - figure out scalings 
	// - what were other channels used for in mathematica script
	// - what is alignment of flux gate w/r global coords (it measures x,y,z but what is mapping to global x,y,z)
	cout << measure.Bx << " " << measure.By << " " << measure.Bz << "\n";
	


	return 0;
}
