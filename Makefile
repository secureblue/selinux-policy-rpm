# Makefile for source rpm: selinux-policy
# $Id$
NAME := selinux-policy
SPECFILE = $(firstword $(wildcard *.spec))

include ../common/Makefile.common
