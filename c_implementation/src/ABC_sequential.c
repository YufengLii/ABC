/*
 ============================================================================
 Name        : ABC_sequential.c
 Author      : Ilaria Malinconico
 Version     :
 Copyright   : Your copyright notice
 Description : Hello World in C, Ansi-style
 ============================================================================
 */

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "ABC_sequential_lib.h"


// int factor = (int) beta * n;

int main(void) {
	// puts("Angle Based Clustering Program - Sequential");
	FILE* file = fopen("../data/dataset_v3_half.csv", "r");
	int x, y, counter = 0, factor = BETA * N;
	int points[N][2], knnPoint[K][2], borderPoints[factor][2];
	float meanPoint[2], directionalAnglesPoint[K], enclosingAnglesPoint[N], borderDegreesPoint[N];

	if (file == NULL) {
		printf("Could not open file.");
		exit(OPEN_FILE_ERROR);
	}

	// creates array of points
	for (int i = 0; i < N; i++) {
		fscanf(file, "%d,%d", &x, &y);
		points[i][0] = x;
		points[i][1] = y;
	}

	for (int i = 0; i < N; i++) {
		// finds k nearest neighbors for each point and the mean point
		getNeighbors(points, points[i][0], points[i][1], knnPoint, meanPoint);

		// finds directional angles between the center, its k nearest neighbors and the mean point
		for (int j = 0; j < K; j++) {
			directionalAnglesPoint[j] = getDirectionalAngle(points[i], meanPoint, knnPoint[j]);
		}

		// finds the enclosing angle for each point and the border degree
		enclosingAnglesPoint[i] = getEnclosingAngle(directionalAnglesPoint);
		borderDegreesPoint[i] = getBorderDegree(directionalAnglesPoint);

		// finds size of border points array
		if (isBorderPoint(enclosingAnglesPoint[i]) == 1) {
			++counter;
		}
	}

	float borderPointsAll[counter][3];
	int counterBis = 0;

	for (int i = 0; i < N; i++) {
		// finds all border points
		if (isBorderPoint(enclosingAnglesPoint[i]) == 1) {
			borderPointsAll[counterBis][0] = points[i][0];
			borderPointsAll[counterBis][1] = points[i][1];
			borderPointsAll[counterBis][2] = borderDegreesPoint[i];
			counterBis++;
		}
	}

	// get factor border points
	getBorderPoints(borderPointsAll, counter, borderPoints, factor);

	int labels[factor];
	for (int i = 0; i < factor; i++) {
		labels[i] = 0;
	}
	// get label for each border point
	getLabelsBorderPoints(borderPoints, factor, 18000, 3, labels);

	return 0;
}
