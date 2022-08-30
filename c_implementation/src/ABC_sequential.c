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
	FILE *file = fopen("../data/dataset_v3_half.csv", "r");
	FILE *output = fopen("../results/results.txt", "w");
	int x, y, counter = 0, counterBis = 0, factor = BETA * N;
	int **ptrPoints, **ptrKnnPoint, **ptrBorderPoints, *ptrLabels;
	float *ptrMeanPoint, *ptrDirectionalAnglesPoint, *ptrEnclosingAnglesPoint, *ptrBorderDegreesPoint, **ptrBorderPointsAll;

	if (file == NULL) {
		printf("Could not open file.\n");
		exit(OPEN_FILE_ERROR);
	}

	ptrPoints = calloc(N, sizeof(int *));
	if (ptrPoints == NULL) {
		printf("Could not allocate memory to pointer.\n");
		exit(MEMORY_ALLOCATION_ERROR);
	} else {
		for (int i = 0; i < N; i++) {
			ptrPoints[i] = calloc(2, sizeof(int));
			if (ptrPoints[i] == NULL) {
				printf("Could not allocate memory to pointer.\n");
				exit(MEMORY_ALLOCATION_ERROR);
			}
		}
	}

	// creates array of points
	for (int i = 0; i < N; i++) {
		fscanf(file, "%d,%d", &x, &y);
		ptrPoints[i][0] = x;
		ptrPoints[i][1] = y;
	}

	ptrEnclosingAnglesPoint = calloc(K, sizeof(float));
	if (ptrEnclosingAnglesPoint == NULL) {
		printf("Could not allocate memory to pointer.\n");
		exit(MEMORY_ALLOCATION_ERROR);
	}

	ptrBorderDegreesPoint = calloc(K, sizeof(float));
	if (ptrBorderDegreesPoint == NULL) {
		printf("Could not allocate memory to pointer.\n");
		exit(MEMORY_ALLOCATION_ERROR);
	}

	for (int i = 0; i < N; i++) {
		ptrKnnPoint = calloc(K, sizeof(int *));
		if (ptrKnnPoint == NULL) {
			printf("Could not allocate memory to pointer.\n");
			exit(MEMORY_ALLOCATION_ERROR);
		} else {
			for (int i = 0; i < K; i++) {
				ptrKnnPoint[i] = calloc(2, sizeof(int));
				if (ptrKnnPoint[i] == NULL) {
					printf("Could not allocate memory to pointer.\n");
					exit(MEMORY_ALLOCATION_ERROR);
				}
			}
		}

		ptrMeanPoint = calloc(2, sizeof(float));
		if (ptrMeanPoint == NULL) {
			printf("Could not allocate memory to pointer.\n");
			exit(MEMORY_ALLOCATION_ERROR);
		}
		// finds k nearest neighbors for each point and the mean point
		getNeighbors(ptrPoints, ptrPoints[i][0], ptrPoints[i][1], ptrKnnPoint, ptrMeanPoint);
		for (int g = 0; g < K; g++) {
			if (ptrKnnPoint[g][0] != 0 && ptrKnnPoint[g][1] != 0) {
				// printf ("%d, %d\n", ptrKnnPoint[g][0], ptrKnnPoint[g][1]);
				fprintf (output, "%d, %d\n", ptrKnnPoint[g][0], ptrKnnPoint[g][1]);
			}
		}
		// printf("\n");
		fprintf(output, "\n");

		ptrDirectionalAnglesPoint = calloc(K, sizeof(float));
		if (ptrDirectionalAnglesPoint == NULL) {
			printf("Could not allocate memory to pointer.\n");
			exit(MEMORY_ALLOCATION_ERROR);
		}

		// finds directional angles between the center, its k nearest neighbors and the mean point
		for (int j = 0; j < K; j++) {
			ptrDirectionalAnglesPoint[j] = getDirectionalAngle(ptrPoints[i], ptrMeanPoint, ptrKnnPoint[j]);
		}

		// finds the enclosing angle for each point and the border degree
		ptrEnclosingAnglesPoint[i] = getEnclosingAngle(ptrDirectionalAnglesPoint);
		ptrBorderDegreesPoint[i] = getBorderDegree(ptrDirectionalAnglesPoint);

		free(ptrDirectionalAnglesPoint);

		// finds size of border points array
		if (isBorderPoint(ptrEnclosingAnglesPoint[i]) == 1) {
			++counter;
		}

		free(ptrKnnPoint);
		free(ptrMeanPoint);
	}

	ptrBorderPointsAll = calloc(counter, sizeof(float *));
	if (ptrBorderPointsAll == NULL) {
		printf("Could not allocate memory to pointer.\n");
		exit(MEMORY_ALLOCATION_ERROR);
	} else {
		for (int i = 0; i < counter; i++) {
			ptrBorderPointsAll[i] = calloc(3, sizeof(float));
			if (ptrBorderPointsAll[i] == NULL) {
				printf("Could not allocate memory to pointer.\n");
				exit(MEMORY_ALLOCATION_ERROR);
			}
		}
	}

	for (int i = 0; i < N; i++) {
		// finds all border points
		if (isBorderPoint(ptrEnclosingAnglesPoint[i]) == 1) {
			ptrBorderPointsAll[counterBis][0] = ptrPoints[i][0];
			ptrBorderPointsAll[counterBis][1] = ptrPoints[i][1];
			ptrBorderPointsAll[counterBis][2] = ptrBorderDegreesPoint[i];
			counterBis++;
		}
	}

	free(ptrPoints);
	free(ptrEnclosingAnglesPoint);
	free(ptrBorderDegreesPoint);

	ptrBorderPoints = calloc(factor, sizeof(int *));
	if (ptrBorderPoints == NULL) {
		printf("Could not allocate memory to pointer.\n");
		exit(MEMORY_ALLOCATION_ERROR);
	} else {
		for (int i = 0; i < factor; i++) {
			ptrBorderPoints[i] = calloc(2, sizeof(float));
			if (ptrBorderPoints[i] == NULL) {
				printf("Could not allocate memory to pointer.\n");
				exit(MEMORY_ALLOCATION_ERROR);
			}
		}
	}

	// get factor border points
	getBorderPoints(ptrBorderPointsAll, counter, ptrBorderPoints, factor);

	free(ptrBorderPointsAll);

	ptrLabels = calloc(factor, sizeof(int));
	if (ptrLabels == NULL) {
		printf("Could not allocate memory to pointer.\n");
		exit(MEMORY_ALLOCATION_ERROR);
	}

	// get label for each border point
	getLabelsBorderPoints(ptrBorderPoints, factor, 18000, 3, ptrLabels);

	free(ptrBorderPoints);

	for (int i = 0; i < factor; i++) {
		printf("label %d : %d\n", i, ptrLabels[i]);
	}

	free(ptrLabels);

	fclose(output);
	return 0;
}
