
def append_crc32(data, exclude_start=0, exclude_end=4):
    """
    Calculates the CRC-32 for the input byte array, excluding a specific range of bytes,
    and appends the 4 CRC bytes in big-endian order.

    Args:
        data (bytes): The input byte array.
        exclude_start (int): The starting index of the range to exclude (inclusive).
        exclude_end (int): The ending index of the range to exclude (exclusive).

    Returns:
        bytes: A new byte array with the original data and the 4-byte CRC appended.
    """
    poly = 0xEDB88320  # Reversed CRC-32 polynomial
    crc = 0xFFFFFFFF   # Initial CRC value

    # Calculate CRC-32, skipping the excluded range
    for i, byte in enumerate(data):
        if exclude_start <= i < exclude_end:
            continue  # Skip bytes in the excluded range

        crc ^= byte  # XOR the byte into the CRC
        for _ in range(8):  # Process each bit
            if crc & 1:  # Check the least significant bit
                crc = (crc >> 1) ^ poly  # XOR with polynomial if LSB is 1
            else:
                crc >>= 1  # Just shift right

    crc = ~crc & 0xFFFFFFFF  # Final inversion and ensure 32-bit result

    # Convert CRC to 4 bytes (big-endian)
    crc_bytes = crc.to_bytes(4, byteorder='big')

    # Return the original data with the CRC appended
    return data + crc_bytes

def print_byte_array_as_hex(byte_array):
    """
    Prints a byte array in hexadecimal format.

    Args:
        byte_array (bytes): The input byte array.
    """
    hex_representation = ' '.join(f'{byte:02X}' for byte in byte_array)
    print(f"Hex Byte Array: {hex_representation}")