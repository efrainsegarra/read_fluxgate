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
	const int MAXCHANNEL = 7;
	for (double read = -1e5; file.read(reinterpret_cast<char*>(&read), sizeof(read)); ){
		full_data[channel].push_back( read );

		// Reset after 8 channels read
		if( channel == MAXCHANNEL ){
			channel = 0;
			continue;
		}
		channel++;
	}

	// For some reason Georg has factors: 2*5 in front of channel 0, 
	// 2*7 in front of channel 1, and 7000 in front of 2-7 ...
	// ¯\_(ツ)_/¯
	cout << average(full_data[0]) << "\n";

	return 0;
}
