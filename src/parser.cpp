#include <iostream>
#include <fstream>
#include <vector>
#include <map>
#include <numeric>
#include <string>
#include <sstream>

#include "constants.h"

using namespace std;

double average(std::vector<double> const & v ){
	return std::accumulate( v.begin(), v.end() ,0.) / v.size();
}


struct Measure {
	bool   status	= false;	// is fluxgate on or not
	double pos 	= DEFAULT;	// position of fluxgate [cm]
	double ang 	= DEFAULT;	// angular position of fluxgate [deg.]
	double it 	= DEFAULT;	// iteration if repeated measurement
					
	double Bx 	= DEFAULT;	// avg of magnetic field in x [pT]
	double By 	= DEFAULT;	// avg of magnetic field in y [pT]
	double Bz 	= DEFAULT;	// avg of magnetic field in z [pT]
	double eBx 	= DEFAULT;	// std of magnetic field in x [pT]
	double eBy 	= DEFAULT;	// std of magnetic field in y [pT]
	double eBz 	= DEFAULT;	// std of magnetic field in z [pT]
};

void grabMetaData(string s, Measure & measure){
	stringstream ss(s);
	string word;

	// First parse all the '_' information
	string search_cm = "cm";
	string search_ang = "deg";
	string search_it = ".bin";
	while (!ss.eof() ){
		getline(ss, word, '_');

		// Look for on/off 
		if( word == "ON" ) measure.status = true;

		// Look for [cm]
		int cm_pos = word.find(search_cm);
		if( cm_pos != string::npos ) measure.pos = stod(word.substr(0,cm_pos));

		// Look for [ang]
		int ang_pos = word.find(search_ang);
		if( ang_pos != string::npos ) measure.ang = stoi(word.substr(0,ang_pos));

		// Look for [iteration]
		int it_pos = word.find(search_it);
		if( it_pos != string::npos ) measure.it = stoi(word.substr(0,it_pos));
	}
}

int main( int argc, char** argv ){

	if( argc < 2 ){
		cerr << "Invalid number of arguments." <<
		       " Please instead us:\n\t./parser [files]\n";
		return -1;
	}
	
	for( int fileno = 1 ; fileno < argc ; ++fileno ){

		ifstream file (argv[fileno], ios::binary);

		// Initialize measurement:
		Measure measure;

		// Grab meta data from filename:
		// 	fluxgate_ON/OFF_DISTANCEcm_ROTATIONdeg_DOWNSAMPLINGFRAC_NUMDATAPOINTS_ITERATION.bin
		// 	specifically, we grab the status (on/off), the distance (cm), the rotation (deg) and iteration
		grabMetaData( argv[fileno] , measure );

		if( measure.status == false ) continue; // Skip OFF for now
		if( measure.it > 0 ) continue; 		// Skip other iterations for now

		/////////////////////////////////////////////////
		// File structure in binary:
		// 	each measurement is a series of 8 double-
		// 	precision numbers, 1 for each readout
		// 	channel
		// 	
		std::map<int,std::vector<double>> full_data;
		int channel = 0;
		for (double read = DEFAULT; file.read(reinterpret_cast<char*>(&read), sizeof(read)); ){

			if( read != DEFAULT) full_data[channel].push_back( SCALING[channel] * read );

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
		// however, the (x,y,z) orientation is rotated w/r lab system
		// 	fluxgate x = lab -y
		// 	fluxgate y = lab -z
		// 	fluxgate z = lab x
		measure.Bx 	=  1 * average(full_data[2]);
		measure.By 	= -1 * average(full_data[0]);
		measure.Bz 	= -1 * average(full_data[1]);

		cout 	<< measure.pos << " " << measure.ang << " " << measure.it << " " 
			<< measure.Bx << " " << measure.By << " " << measure.Bz << "\n";
	}
	



	


	return 0;
}
