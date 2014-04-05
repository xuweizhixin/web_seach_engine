/* VByte.h
 * Copyright (C) 2012, Francisco Claude & Rodrigo Canovas & Miguel A. Martinez-Prieto
 * all rights reserved.
 *
 * This class implements the Variable Byte (VByte) Code.
 *
 *   ==========================================================================
 *     "Compressing integers for fast file access"
 *     Hugh Williams and Justin Zobel.
 *     The Computer Journal 42, p.193-201, 1999.
 *   ==========================================================================
 *
 * This library is free software; you can redistribute it and/or
 * modify it under the terms of the GNU Lesser General Public
 * License as published by the Free Software Foundation; either
 * version 2.1 of the License, or (at your option) any later version.
 *
 * This library is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 * Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public
 * License along with this library; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
 *
 *
 * Contacting the authors:
 *   Francisco Claude:  	fclaude@cs.uwaterloo.ca
 *   Rodrigo Canovas:  		rcanovas@student.unimelb.edu.au
 *   Miguel A. Martinez-Prieto:	migumar2@infor.uva.es
 */


#ifndef _VBYTE_H
#define _VBYTE_H

#include <stdint.h>
#include <iostream>

class VByte {		
  public:
    /** Encodes the integer 'c' in the sequence of bytes (uchar) 'r'.
	@c: number to be encoded.
	@r: encoded sequence.
	@return: the number of bytes used for encoding.
    */
    static uint32_t encode(uint64_t c, uint8_t *r);

    /** Decodes the sequence of bytes (uchar) 'r' into the integer 'c'.
	@c: decoded number.
	@r: sequence to be decoded.
	@return: the number of bytes read for decoding.
    */
    static uint32_t decode(uint64_t *c, uint8_t *r);
};

#endif  /* _VBYTE_H */

