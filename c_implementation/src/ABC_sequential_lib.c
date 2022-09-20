/*
 * ABC_sequential.h
 *
 *  Created on: 25 giu 2022
 *      Author: ilaria
 */

#ifndef ABC_SEQUENTIAL_H_
#define ABC_SEQUENTIAL_H_
#endif /* ABC_SEQUENTIAL_H_ */

#define K 12
#define BETA 0.2
#define N 500

#define OPEN_FILE_ERROR -1
#define MEMORY_ALLOCATION_ERROR -2

#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif // M_PI

// MISCELLANEOUS

void printErrorAllocation() {
	printf("Could not allocate memory to pointer.\n");
	exit(MEMORY_ALLOCATION_ERROR);
}

// KNN methods

float euclideanDistance(int x1, int y1, int x2, int y2) {
	return sqrtf(pow(x2 - x1, 2) + pow(y2 - y1, 2));
}

void sortArrayDistances(float **distancesPoints) {
	float tmp[3];

	for (int i = 0; i < N-1; i++) {
		for (int j = i + 1; j < N; j++) {
			if (distancesPoints[i][2] > distancesPoints[j][2]) {
				tmp[0] = distancesPoints[i][0];
				tmp[1] = distancesPoints[i][1];
				tmp[2] = distancesPoints[i][2];
				distancesPoints[i][0] = distancesPoints[j][0];
				distancesPoints[j][0] = tmp[0];
				distancesPoints[i][1] = distancesPoints[j][1];
				distancesPoints[j][1] = tmp[1];
				distancesPoints[i][2] = distancesPoints[j][2];
				distancesPoints[j][2] = tmp[2];
			}
		}
	}
}

// non permette di ritornare un array, ma si può ritornare il puntatore all'array specificandone il nome senza indice
void getNeighbors(int **points, int x, int y, int **knn, float *meanPoint) {
	// non ritorna l'indirizzo di una variabile locale all'esterno della funzione, quindi serve static nella definizione della variabile locale
	float **distances;
	float tmp_x = 0.00, tmp_y = 0.00;
	int i, j;

	distances = calloc(N, sizeof(float *));
	if (distances == NULL) {
		printErrorAllocation();
	} else {
		for (int i = 0; i < N; i++) {
			distances[i] = calloc(3, sizeof(float));
			if (distances[i] == NULL) {
				printErrorAllocation();
			}
		}
	}

	for (i = 0; i < N; i++) {
		float distance = euclideanDistance(x, y, points[i][0], points[i][1]);
		for (j = 0; j < 3; j++) {
			if (j != 2) {
				distances[i][j] = points[i][j];
			} else {
				distances[i][j] = distance;
			}
		}
	}

	sortArrayDistances(distances);

	for (i = 0; i < K; i++) {
		knn[i][0] = distances[i+1][0];
		knn[i][1] = distances[i+1][1];
	}

	free(distances);

	for (i = 0; i < K; i++) {
		tmp_x += knn[i][0];
		tmp_y += knn[i][1];
	}

	meanPoint[0] = tmp_x / K;
	meanPoint[1] = tmp_y / K;
}

// ENCLOSING ANGLES

float getDirectionalAngle(int *center, float *meanPoint, int *neighbor) {
	float uX = 0.00, uY = 0.00, vX = 0.00, vY = 0.00, directionalAngle = 0.00, directionalAngleDegree = 0.00;

	// mean point - center
	uX = meanPoint[0] - center[0];
	uY = meanPoint[1] - center[1];

	// neighbor - center
	vX = neighbor[0] - center[0];
	vY = neighbor[1] - center[1];

	directionalAngle = atan2(vY, vX) - atan2(uY, uX);
	directionalAngleDegree = directionalAngle * (180 / M_PI);

	if (directionalAngleDegree < 0) {
		directionalAngleDegree += 360;
	}

	return directionalAngleDegree;
}

int findSize(float *directionalAngles) {
	int counter = 0;
	for (int i = 0; i < K; i++) {
		if (directionalAngles[i] >= 180) {
			++counter;
		}
	}
	return counter;
}

float getEnclosingAngle(float *directionalAngles) {
	int sizeTmp = findSize(directionalAngles), i;
	float tmpDirectionalAngles[sizeTmp], enclosingAngle = 0.00;
	int counter = 0;
	for (i = 0; i < K; i++) {
		if (directionalAngles[i] >= 180) {
			tmpDirectionalAngles[counter] = directionalAngles[i];
			++counter;
		}
	}

	float minimumAngle = tmpDirectionalAngles[0];
	for (i = 0; i < sizeTmp; i++) {
		if (minimumAngle > tmpDirectionalAngles[i]) {
			minimumAngle = tmpDirectionalAngles[i];
		}
	}

	enclosingAngle = 360 - minimumAngle;
	return enclosingAngle;
}

float getBorderDegree(float *directionalAngles) {
	float minimumAngle = directionalAngles[0], borderDegree = 0.00;
	for (int i = 0; i < K; i++) {
		if (minimumAngle > directionalAngles[i]) {
			minimumAngle = directionalAngles[i];
		}
	}

	borderDegree = 360 - minimumAngle;
	return borderDegree;
}

int isBorderPoint(float enclosingAngle) {
	if (enclosingAngle < 60) {
		return 1;
	} else {
		return 0;
	}
}

void sortArrayBorderDegrees(float **borderDegrees) {
	float tmp[3];

	for (int i = 0; i < N-1; i++) {
		for (int j = i + 1; j < N; j++) {
			if (borderDegrees[i][2] < borderDegrees[j][2]) {
				tmp[0] = borderDegrees[i][0];
				tmp[1] = borderDegrees[i][1];
				tmp[2] = borderDegrees[i][2];
				borderDegrees[i][0] = borderDegrees[j][0];
				borderDegrees[j][0] = tmp[0];
				borderDegrees[i][1] = borderDegrees[j][1];
				borderDegrees[j][1] = tmp[1];
				borderDegrees[i][2] = borderDegrees[j][2];
				borderDegrees[j][2] = tmp[2];
			}
		}
	}
}

void getBorderPoints(float **borderPointsAll, int sizeArray, int **borderPoints) {
	sortArrayBorderDegrees(borderPointsAll);
	for (int i = 0; i < sizeArray; i++) {
		borderPoints[i][0] = borderPointsAll[i][0];
		borderPoints[i][1] = borderPointsAll[i][1];
	}

}

// DBSCAN

float moduleVector(int x, int y) {
	return sqrt(pow(x, 2) + pow(y, 2));
}

float directionAngleModifiedDistanceFunction(int aX, int aY, int bX, int bY) {
	double product = 0.00;
	float angleBetweenVectors = 0.00;
	product = (double) aX * (double) bX + (double) aY * (double) bY;
	angleBetweenVectors = product / (moduleVector(aX, aY) * moduleVector(bX, bY));
	return euclideanDistance(aX, aY, bX, bY) * (1 + ((0.5 - 1) / M_PI) * angleBetweenVectors);
}

int regionQuery(int **borderPoints, int **neighbors, int factor, int x, int y, int epsilon) {
	int counter = 0;
	for (int i = 0; i < factor; i++) {
		float disComputed = directionAngleModifiedDistanceFunction(x, y, borderPoints[i][0], borderPoints[i][1]);
		if (disComputed < epsilon) {
			neighbors[counter][0] = i;
			neighbors[counter][1] = borderPoints[i][0];
			neighbors[counter][2] = borderPoints[i][1];
			++counter;
		}
	}
	return counter;
}

int checkIfAlreadyNeighbor(int **neighbors, int lenNeighbors, int *index) {
	int flag = 0;
	for (int i = 0; i < lenNeighbors; i++) {
		if (neighbors[i][0] >= 0) {
			if (neighbors[i][1] == index[1] && neighbors[i][2] == index[2]) {
				flag = 1;
				break;
			}
		}
	}
	return flag;
}

void growCluster(int **borderPoints, int factor, int *labels, int index, int x, int y, int **neighbors, int lenNeighbors, int clusterId, int epsilon, int minNumberPoints) {
	labels[index] = clusterId;
	int counter = 0, i, j, neighborsIncrement;
	int **ptrNextNeighbors;

	ptrNextNeighbors = calloc(factor, sizeof(int *));
	if (ptrNextNeighbors == NULL) {
		printErrorAllocation();
	} else {
		for (i = 0; i < factor; i++) {
			ptrNextNeighbors[i] = calloc(3, sizeof(float));
			if (ptrNextNeighbors[i] == NULL) {
				printErrorAllocation();
			}
		}
	}

	while (counter < lenNeighbors) {
		int lenNextNeighbors = 0;
		if (counter != 0) {
			for (j = 0; j < factor; j++) {
				ptrNextNeighbors[j][0] = 0;
				ptrNextNeighbors[j][1] = 0;
				ptrNextNeighbors[j][2] = 0;
			}
		}
		int next_index = neighbors[counter][0];
		if (labels[next_index] == -1) {
			labels[next_index] = clusterId;
		} else if (labels[next_index] == 0) {
			labels[next_index] = clusterId;
			lenNextNeighbors = regionQuery(borderPoints, ptrNextNeighbors, factor, borderPoints[next_index][0], borderPoints[next_index][1], epsilon);
			if (lenNextNeighbors >= minNumberPoints) {
				neighborsIncrement = 0;
				for (i = 0; i < lenNextNeighbors; i++) {
					if (checkIfAlreadyNeighbor(neighbors, lenNeighbors, ptrNextNeighbors[i]) == 0) {
						neighbors[lenNeighbors + neighborsIncrement][0] = ptrNextNeighbors[i][0];
						neighbors[lenNeighbors + neighborsIncrement][1] = ptrNextNeighbors[i][1];
						neighbors[lenNeighbors + neighborsIncrement][2] = ptrNextNeighbors[i][2];
						++lenNeighbors;
						++neighborsIncrement;
					}
				}
			}
		}
		++counter;
	}
	free(ptrNextNeighbors);
}

void getLabelsBorderPoints(int **borderPoints, int factor, int epsilon, int minNumberPoints, int *labels) {
	int clusterId = 0, i, j;
	int **ptrNeighbors;

	ptrNeighbors = calloc(factor, sizeof(int *));
	if (ptrNeighbors == NULL) {
		printErrorAllocation();
	} else {
		for (i = 0; i < factor; i++) {
			ptrNeighbors[i] = calloc(3, sizeof(float));
			if (ptrNeighbors[i] == NULL) {
				printErrorAllocation();
			}
		}
	}

	for (i = 0; i < factor; i++) {
		int lenNeighbors = 0;
		if (i != 0) {
			for (j = 0; j < factor; j++) {
				ptrNeighbors[j][0] = 0;
				ptrNeighbors[j][1] = 0;
				ptrNeighbors[j][2] = 0;
			}
		}
		if (labels[i] == 0) {
			lenNeighbors = regionQuery(borderPoints, ptrNeighbors, factor, borderPoints[i][0], borderPoints[i][1], epsilon);
			if (lenNeighbors < minNumberPoints) {
				labels[i] = -1;
			} else {
				++clusterId;
				growCluster(borderPoints, factor, labels, i, borderPoints[i][0], borderPoints[i][1], ptrNeighbors, lenNeighbors, clusterId, epsilon, minNumberPoints);
			}
		}
	}

	free(ptrNeighbors);
}

// CLUSTER

int checkIfBorderPoint(int **borderPoints, int factor, int x, int y) {
	for (int i = 0; i < factor; i++) {
		if (borderPoints[i][0] == x && borderPoints[i][1] == y) {
			return 1;
		}
	}
	return 0;
}

void getNonBorderPoints(int **points, int **borderPoints, int factor, int **nonBorderPoints) {
	int counter = 0;
	for (int i = 0; i < N; i++) {
		if (checkIfBorderPoint(borderPoints, factor, points[i][0], points[i][1]) == 0) {
			nonBorderPoints[counter][0] = points[i][0];
			nonBorderPoints[counter][1] = points[i][1];
			++counter;
		}
	}
}

float findMinimumDistance(float **distances, int factor) {
	float minimumDistance = 0.0;
	for (int i = 0; i < factor; i++) {
		if (i == 0) {
			minimumDistance = distances[i][0];
		} else {
			if (minimumDistance > distances[i][0] && distances[i][0] != 0.00) {
				minimumDistance = distances[i][0];
			}
		}
	}
	return minimumDistance;
}

void getLabelsNonBorderPoints(int **borderPoints, int factor, int *labels, int **nonBorderPoints, int otherFactor, int *nonBorderLabels) {
	float **distancesAndLabels, minDistance;
	int labelMin;

	distancesAndLabels = calloc(factor, sizeof(int *));
	if (distancesAndLabels == NULL) {
		printErrorAllocation();
	} else {
		for (int k = 0; k < factor; k++) {
			distancesAndLabels[k] = calloc(2, sizeof(float));
			if (distancesAndLabels[k] == NULL) {
				printErrorAllocation();
			}
		}
	}

	for (int i = 0; i < otherFactor; i++) {
		minDistance = 0.0;
		labelMin = 0;
		if (i != 0) {
			for (int h = 0; h < factor; h++) {
				distancesAndLabels[h][0] = 0;
				distancesAndLabels[h][1] = 0;
			}
		}
		for (int j = 0; j < factor; j++) {
			if (labels[j] != -1) {
				distancesAndLabels[j][0] = directionAngleModifiedDistanceFunction(nonBorderPoints[i][0], nonBorderPoints[i][1], borderPoints[j][0], borderPoints[j][1]);
				distancesAndLabels[j][1] = labels[j];
			}
		}
		minDistance = findMinimumDistance(distancesAndLabels, factor);
		for (int k = 0; k < factor; k++) {
			if ((minDistance == distancesAndLabels[k][0]) && (distancesAndLabels[k][1] != -1)) {
				labelMin = distancesAndLabels[k][1];
				break;
			}
		}
		nonBorderLabels[i] = labelMin;
	}

	free(distancesAndLabels);
}
