#ifndef __CONSTANTS_H__
#define __CONSTANTS_H__

const double 	DEFAULT = -1e5;
const int 	EXPECTEDSIZE = 10000;

const int 	MAXCHANNEL = 7;
const double 	SCALING[MAXCHANNEL+1] = { 1E3 * 1E4, 1E3 * 1E4, 1E3 * 1E4, 0., 0., 0., 0., 0. };
		// 10000 nT/V scaling of fluxgate with 1E3 pT/nT 
#endif
