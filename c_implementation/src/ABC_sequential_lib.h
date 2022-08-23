/*
 * ABC_sequential.h
 *
 *  Created on: 25 giu 2022
 *      Author: ilaria
 */

#define K 12
#define BETA 0.2
#define N 500

#define OPEN_FILE_ERROR -1

// KNN methods
float euclideanDistance(int x1, int y1, int x2, int y2);
void sortArrayDistances(float distancesPoints[][3]);
void getNeighbors(int points[][2], int x, int y, int knn[][2], float meanPoint[2]);

// ENCLOSING ANGLES
float getDirectionalAngle(int center[2], float meanPoint[2], int neighbor[2]);
int findSize(float directionalAngles[K]);
float getEnclosingAngle(float directionalAngles[K]);
float getBorderDegree(float directionalAngles[K]);
int isBorderPoint(float enclosingAngle);
void sortArrayBorderDegrees(float borderDegrees[], int sizeArray);
void getBorderPoints(float borderPointsAll[][3], int sizeArray, int borderPoints[][2], int factor);
int scalarProduct(int aX, int aY, int bX, int bY);
float moduleVector(int x, int y);
float angleBetweenVectors(int aX, int aY, int bX, int bY);
float directionAngleModifiedDistanceFunction(int aX, int aY, int bX, int bY);
int regionQuery(int borderPoints[][2], int neighbors[][3], int factor, int x, int y, int epsilon);
void growCluster(int borderPoints[][2], int factor, int labels[], int index, int x, int y, int neighbors[][3], int lenNeighbors, int clusterId, int epsilon, int minNumberPoints);
void getLabelsBorderPoints(int borderPoints[][2], int factor, int epsilon, int minNumberPoints, int labels[]);
