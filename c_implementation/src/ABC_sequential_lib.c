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

#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif // M_PI

// KNN methods

float euclideanDistance(int x1, int y1, int x2, int y2) {
	return sqrtf(pow(x2 - x1, 2) + pow(y2 - y1, 2));
}

void sortArrayDistances(float distancesPoints[][3]) {
	for (int i = 0; i < N-1; i++) {
		for (int j = i + 1; j < N; j++) {
			if (distancesPoints[i][2] > distancesPoints[j][2]) {
				int tmp = distancesPoints[i][2];
				distancesPoints[i][2] = distancesPoints[j][2];
				distancesPoints[j][2] = tmp;
			}
		}
	}
}

// non permette di ritornare un array, ma si può ritornare il puntatore all'array specificandone il nome senza indice
void getNeighbors(int points[][2], int x, int y, int knn[][2], float meanPoint[2]) {
	// non ritorna l'indirizzo di una variabile locale all'esterno della funzione, quindi serve static nella definizione della variabile locale
	float distances[N][3];
	float tmp_x = 0.00, tmp_y = 0.00;

	for (int i = 0; i < N; i++) {
		float distance = euclideanDistance(x, y, points[i][0], points[i][1]);
		for (int j = 0; j < 3; j++) {
			if (j != 2) {
				distances[i][j] = points[i][j];
			} else {
				distances[i][j] = distance;
			}
		}
	}

	sortArrayDistances(distances);

	for (int i = 1; i <= K; i++) {
		knn[i-1][0] = distances[i][0];
		knn[i-1][1] = distances[i][1];
	}

	for (int i = 0; i < K; i++) {
		tmp_x += knn[i][0];
		tmp_y += knn[i][1];
	}

	meanPoint[0] = tmp_x / K;
	meanPoint[1] = tmp_y / K;
}

// ENCLOSING ANGLES

float getDirectionalAngle(int center[2], float meanPoint[2], int neighbor[2]) {
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

int findSize(float directionalAngles[K]) {
	int counter = 0;
	for (int i = 0; i < K; i++) {
		if (directionalAngles[i] >= 180) {
			++counter;
		}
	}
	return counter;
}

float getEnclosingAngle(float directionalAngles[K]) {
	int sizeTmp = findSize(directionalAngles);
	float tmpDirectionalAngles[sizeTmp], enclosingAngle = 0.00;
	int counter = 0;
	for (int i = 0; i < K; i++) {
		if (directionalAngles[i] >= 180) {
			tmpDirectionalAngles[counter] = directionalAngles[i];
			++counter;
		}
	}

	float minimumAngle = tmpDirectionalAngles[0];
	for (int i = 0; i < sizeTmp; i++) {
		if (minimumAngle > tmpDirectionalAngles[i]) {
			minimumAngle = tmpDirectionalAngles[i];
		}
	}

	enclosingAngle = 360 - minimumAngle;
	return enclosingAngle;
}

float getBorderDegree(float directionalAngles[K]) {
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

void sortArrayBorderDegrees(float borderDegrees[][3], int sizeArray) {
	for (int i = 0; i < sizeArray-1; i++) {
			for (int j = i + 1; j < sizeArray; j++) {
				if (borderDegrees[i][2] < borderDegrees[j][2]) {
					float tmp = borderDegrees[i][2];
					borderDegrees[i][2] = borderDegrees[j][2];
					borderDegrees[j][2] = tmp;
				}
			}
		}
}

void getBorderPoints(float borderPointsAll[][3], int sizeArray, int borderPoints[][2], int factor) {
	sortArrayBorderDegrees(borderPointsAll, sizeArray);

	for (int i = 0; i < factor; i++) {
		borderPoints[i][0] = borderPointsAll[i][0];
		borderPoints[i][1] = borderPointsAll[i][1];
	}

}

int scalarProduct(int aX, int aY, int bX, int bY) {
	return aX * bX + aY * bY;
}

float moduleVector(int x, int y) {
	return sqrt(pow(x, 2) + pow(y, 2));
}

float angleBetweenVectors(int aX, int aY, int bX, int bY) {
	return scalarProduct(aX, aY, bX, bY) / (moduleVector(aX, aY) * moduleVector(bX, bY));
}

float directionAngleModifiedDistanceFunction(int aX, int aY, int bX, int bY) {
	// printf("distance is : %0.2f\n", euclideanDistance(aX, aY, bX, bY) * (1 + ((0.5 - 1) / M_PI) * angleBetweenVectors(aX, aY, bX, bY)));
	return euclideanDistance(aX, aY, bX, bY) * (1 + ((0.5 - 1) / M_PI) * angleBetweenVectors(aX, aY, bX, bY));
}

int regionQuery(int borderPoints[][2], int neighbors[][3], int factor, int x, int y, int epsilon) {
	// printf("region query\n");
	int counter = 0;
	for (int i = 0; i < factor; i++) {
		float disComputed = directionAngleModifiedDistanceFunction(x, y, borderPoints[i][0], borderPoints[i][1]);
		if (x != borderPoints[i][0] && y != borderPoints[i][1]) {
			if (disComputed < epsilon && disComputed != 0.00) {
				/*printf("distance < epsilon\n");
				printf("x : %d\n", borderPoints[i][0]);
				printf("y : %d\n", borderPoints[i][1]);*/
				neighbors[counter][0] = i;
				neighbors[counter][1] = borderPoints[i][0];
				neighbors[counter][2] = borderPoints[i][1];
				++counter;
			}
		}
	}
	return counter;
}

int checkIfAlreadyNeighbor(int neighbors[][3], int lenNeighbors, int index[3]) {
	int flag = 0;
	for (int i = 0; i < lenNeighbors; i++) {
		if (neighbors[i][0] >= 0) {
			/*printf("index neighbor (i : %d) : %d\n", i, neighbors[i][0]);
			printf("index : %d\n", index[0]);
			printf("x neighbor (i : %d) : %d\n", i, neighbors[i][1]);
			printf("x : %d\n", index[1]);
			printf("y neighbor (i : %d) : %d\n", i, neighbors[i][2]);
			printf("y : %d\n\n", index[2]);*/
			// if ((neighbors[i][0] == index[0]) || (neighbors[i][1] == index[1] && neighbors[i][2] == index[2])) {
			if (neighbors[i][1] == index[1] && neighbors[i][2] == index[2]) {
				flag = 1;
				break;
			}
		}
	}
	return flag;
}

void growCluster(int borderPoints[][2], int factor, int labels[], int index, int x, int y, int neighbors[][3], int lenNeighbors, int clusterId, int epsilon, int minNumberPoints) {
	labels[index] = clusterId;
	int counter = 0;
	int nextNeighbors[factor][3];
	while (counter < lenNeighbors) {
		if (lenNeighbors <= factor) {
			printf("%d counter : %d\n", index, counter);
			int lenNextNeighbors = 0;
			for (int j = 0; j < factor; j++) {
				nextNeighbors[j][0] = -1;
				nextNeighbors[j][1] = 0;
				nextNeighbors[j][2] = 0;
			}
			int next_index = neighbors[counter][0];
			printf("\tnext index : %d\n", next_index);
			if (next_index != -1) {
				if (labels[next_index] == -1) {
					labels[next_index] = clusterId;
				} else if (labels[next_index] == 0) {
					labels[next_index] = clusterId;
					lenNextNeighbors = regionQuery(borderPoints, nextNeighbors, factor, borderPoints[next_index][0], borderPoints[next_index][1], epsilon);
					if (lenNextNeighbors >= minNumberPoints) {
						for (int i = 0; i < lenNextNeighbors; i++) {
							if (checkIfAlreadyNeighbor(neighbors, lenNeighbors, nextNeighbors[i]) == 0) {
								neighbors[lenNeighbors + i][0] = i;
								neighbors[lenNeighbors + i][1] = nextNeighbors[i][1];
								neighbors[lenNeighbors + i][2] = nextNeighbors[i][2];
								++lenNeighbors;
								printf("\t\tlen neighbors updated : %d\n\n", lenNeighbors);
								if (lenNeighbors >= factor) {
									break;
								}
							}
						}
					}
				}
			}
		} else {
			break;
		}
	// exit(-1);
	++counter;
	}
}

void getLabelsBorderPoints(int borderPoints[][2], int factor, int epsilon, int minNumberPoints, int labels[]) {
	int clusterId = 0;
	int neighbors[factor][3];
	printf("factor is %d\n", factor);
	for (int i = 0; i < factor; i++) {
		printf("\t\t\t\t\tindex i : %d\n", i);
		int lenNeighbors = 0;
		for (int j = 0; j < factor; j++) {
			neighbors[j][0] = -1;
			neighbors[j][1] = 0;
			neighbors[j][2] = 0;
		}
		printf("\t\tcurrent label %d\n", labels[i]);
		if (labels[i] == 0) {
			lenNeighbors = regionQuery(borderPoints, neighbors, factor, borderPoints[i][0], borderPoints[i][1], epsilon);
			/*printf("starting x : %d\n", borderPoints[i][0]);
			printf("starting y : %d\n", borderPoints[i][1]);*/
			printf("len neighbors %d\n", lenNeighbors);
			if (lenNeighbors < minNumberPoints) {
				printf("\t\toutsider\n");
				labels[i] = -1;
			} else {
				printf("\t\tgrow cluster\n");
				++clusterId;
				printf("cluster id is : %d\n", clusterId);
				growCluster(borderPoints, factor, labels, i, borderPoints[i][0], borderPoints[i][1], neighbors, lenNeighbors, clusterId, epsilon, minNumberPoints);
			}
			// exit(-2);
		}
	}
	printf("the end.");
}
