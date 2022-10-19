'use strict';

const {src, dest, watch, series} = require('gulp');
const sass = require('gulp-sass')(require('sass'));
const cssmin = require('gulp-cssmin');
const rename = require('gulp-rename');

exports.sass = function () {
    return src('./static/css/custom.scss')
        .pipe(sass().on('error', sass.logError))
        .pipe(cssmin())
        .pipe(rename({suffix: '.min'}))
        .pipe(dest('./static/dist'));
}

exports.watch = function () {
    watch('./static/css/*.scss', series('sass'));
};