/*
 ============================================================================
 Name        : ABC_sequential.c
 Author      : Ilaria Malinconico
 Version     :
 Copyright   : Your copyright notice
 Description : ABC sequential implementation
 ============================================================================
 */

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "ABC_sequential_lib.h"

int main(void) {
	// puts("Angle Based Clustering Program - Sequential");
	FILE *file = fopen("../data/dataset_v3_half.csv", "r");
	FILE *output = fopen("../results/results.txt", "w");
	int i, j, g, x, y, counter = 0, factor = BETA * N, otherFactor;
	int **ptrPoints, **ptrKnnPoint, **ptrBorderPoints, *ptrLabels, **ptrNonBorderPoints, *ptrNonBorderLabels;
	float *ptrMeanPoint, *ptrDirectionalAnglesPoint, *ptrEnclosingAnglesPoint, *ptrBorderDegreesPoint, **ptrBorderPointsAll;

	if (file == NULL || output == NULL) {
		printf("Could not open file.\n");
		exit(OPEN_FILE_ERROR);
	}

	// --------------------------------------------------- ALLOCAZIONI DI MEMORIA
	ptrPoints = calloc(N, sizeof(int *));
	if (ptrPoints == NULL) {
		printErrorAllocation();
	} else {
		for (i = 0; i < N; i++) {
			ptrPoints[i] = calloc(2, sizeof(int));
			if (ptrPoints[i] == NULL) {
				printErrorAllocation();
			}
		}
	}

	ptrEnclosingAnglesPoint = calloc(K, sizeof(float));
	if (ptrEnclosingAnglesPoint == NULL) {
		printErrorAllocation();
	}

	ptrBorderDegreesPoint = calloc(K, sizeof(float));
	if (ptrBorderDegreesPoint == NULL) {
		printErrorAllocation();
	}

	ptrKnnPoint = calloc(K, sizeof(int *));
	if (ptrKnnPoint == NULL) {
		printErrorAllocation();
	} else {
		for (i = 0; i < K; i++) {
			ptrKnnPoint[i] = calloc(2, sizeof(int));
			if (ptrKnnPoint[i] == NULL) {
				printErrorAllocation();
			}
		}
	}

	ptrMeanPoint = calloc(2, sizeof(float));
	if (ptrMeanPoint == NULL) {
		printErrorAllocation();
	}

	ptrDirectionalAnglesPoint = calloc(K, sizeof(float));
	if (ptrDirectionalAnglesPoint == NULL) {
		printErrorAllocation();
	}

	ptrBorderPointsAll = calloc(N, sizeof(float *));
	if (ptrBorderPointsAll == NULL) {
		printErrorAllocation();
	} else {
		for (i = 0; i < N; i++) {
			ptrBorderPointsAll[i] = calloc(3, sizeof(float));
			if (ptrBorderPointsAll[i] == NULL) {
				printErrorAllocation();
			}
		}
	}

	ptrBorderPoints = calloc(factor, sizeof(int *));
	if (ptrBorderPoints == NULL) {
		printErrorAllocation();
	} else {
		for (i = 0; i < factor; i++) {
			ptrBorderPoints[i] = calloc(2, sizeof(int));
			if (ptrBorderPoints[i] == NULL) {
				printErrorAllocation();
			}
		}
	}

	ptrLabels = calloc(factor, sizeof(int));
	if (ptrLabels == NULL) {
		printErrorAllocation();
	}

	// creates array of points
	for (i = 0; i < N; i++) {
		fscanf(file, "%d,%d", &x, &y);
		ptrPoints[i][0] = x;
		ptrPoints[i][1] = y;
	}

	// --------------------------------------------------- CICLO PER BORDER POINTS
	for (i = 0; i < N; i++) {
		// finds k nearest neighbors for each point and the mean point
		getNeighbors(ptrPoints, ptrPoints[i][0], ptrPoints[i][1], ptrKnnPoint, ptrMeanPoint);
		for (g = 0; g < K; g++) {
			if (ptrKnnPoint[g][0] != 0 && ptrKnnPoint[g][1] != 0) {
				fprintf (output, "%d, %d\n", ptrKnnPoint[g][0], ptrKnnPoint[g][1]);
			}
		}
		fprintf(output, "\n");

		// finds directional angles between the center, its k nearest neighbors and the mean point
		for (j = 0; j < K; j++) {
			ptrDirectionalAnglesPoint[j] = getDirectionalAngle(ptrPoints[i], ptrMeanPoint, ptrKnnPoint[j]);
		}

		// finds the border points with enclosing angle for each point and border degree
		if (isBorderPoint(getEnclosingAngle(ptrDirectionalAnglesPoint)) == 1) {
			ptrBorderPointsAll[counter][0] = ptrPoints[i][0];
			ptrBorderPointsAll[counter][1] = ptrPoints[i][1];
			ptrBorderPointsAll[counter][2] = getBorderDegree(ptrDirectionalAnglesPoint);
			++counter;
		}
	}

	free(ptrEnclosingAnglesPoint);
	free(ptrBorderDegreesPoint);
	free(ptrKnnPoint);
	free(ptrMeanPoint);
	free(ptrDirectionalAnglesPoint);

	// get factor border points
	getBorderPoints(ptrBorderPointsAll, counter, ptrBorderPoints);
	free(ptrBorderPointsAll);

	if (counter < factor) {
		factor = counter;
	}

	// get label for each border point
	getLabelsBorderPoints(ptrBorderPoints, factor, 18000, 3, ptrLabels);

	otherFactor = N - factor;
	ptrNonBorderPoints = calloc(otherFactor, sizeof(int *));
	if (ptrNonBorderPoints == NULL) {
		printErrorAllocation();
	} else {
		for (i = 0; i < otherFactor; i++) {
			ptrNonBorderPoints[i] = calloc(2, sizeof(int));
			if (ptrNonBorderPoints[i] == NULL) {
				printErrorAllocation();
			}
		}
	}

	ptrNonBorderLabels = calloc(otherFactor, sizeof(int));
	if (ptrNonBorderLabels == NULL) {
		printErrorAllocation();
	}

	getNonBorderPoints(ptrPoints, ptrBorderPoints, factor, ptrNonBorderPoints);
	free(ptrPoints);

	getLabelsNonBorderPoints(ptrBorderPoints, factor, ptrLabels, ptrNonBorderPoints, otherFactor, ptrNonBorderLabels);
	free(ptrBorderPoints);
	free(ptrLabels);
	free(ptrNonBorderPoints);
	free(ptrNonBorderLabels);
	fclose(output);
	return 0;
}
