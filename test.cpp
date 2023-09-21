#include <opencv2/opencv.hpp>
#include "windows.h"
#include <fstream>


cv::Mat getParameter(std::string parameter_path)
{
    std::fstream f(parameter_path);
    std::vector<std::string> parameter;
    std::string line;
    if (!f.is_open()) {
        std::cout << "unable to open" << std::endl;
    }
    std::vector<std::vector<float>> data;
    std::string line;
    while (std::getline(f, line)) {
        std::vector<float> row;
        std::istringstream iss(line);
        float value;
        while (iss >> value) {
            row.push_back(value);
        }
        data.push_back(row);
    }

    f.close();
    int rows = data.size();
    int cols = data[0].size();
    cv::Mat shadingratio(rows, cols, CV_32F);
    for (int i = 0; i < rows; ++i) {
        for (int j = 0; j < cols; ++j) {
            shadingratio.at<float>(i, j) = data[i][j];
        }
    }
    return shadingratio;
}

cv::Mat CorrectImage(cv::Mat& srcImage, std::string parameter_path)
{
    cv::Mat image;
    cv::Mat grayImage;
    cv::cvtColor(srcImage, grayImage, cv::COLOR_BGR2GRAY);
    grayImage.convertTo(image, CV_32F);

    cv::Mat shadingratio = getParameter(parameter_path);
    cv::Mat result;
    cv::divide(image, shadingratio, result);

    cv::Mat colorImage;
    cv::cvtColor(result, colorImage, cv::COLOR_GRAY2BGR);

    cv::Mat clippedImage;
    cv::threshold(colorImage, clippedImage, 0, 255, cv::THRESH_TOZERO);
    cv::threshold(clippedImage, clippedImage, 255, 255, cv::THRESH_TRUNC);

    return clippedImage;
}