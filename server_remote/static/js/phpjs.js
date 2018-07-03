/**
 * Created by evolution on 16-12-6.
 */

function array_key_exists(key, search) {
    //  discuss at: http://phpjs.org/functions/array_key_exists/
    // original by: Kevin van Zonneveld (http://kevin.vanzonneveld.net)
    // improved by: Felix Geisendoerfer (http://www.debuggable.com/felix)
    //   example 1: array_key_exists('kevin', {'kevin': 'van Zonneveld'});
    //   returns 1: true

    if (!search || (search.constructor !== Array && search.constructor !== Object)) {
        return false;
    }

    return key in search;
}

function array_push(inputArr) {
    //  discuss at: http://phpjs.org/functions/array_push/
    // original by: Kevin van Zonneveld (http://kevin.vanzonneveld.net)
    // improved by: Brett Zamir (http://brett-zamir.me)
    //        note: Note also that IE retains information about property position even
    //        note: after being supposedly deleted, so if you delete properties and then
    //        note: add back properties with the same keys (including numeric) that had
    //        note: been deleted, the order will be as before; thus, this function is not
    //        note: really recommended with associative arrays (objects) in IE environments
    //   example 1: array_push(['kevin','van'], 'zonneveld');
    //   returns 1: 3

    var i = 0,
        pr = '',
        argv = arguments,
        argc = argv.length,
        allDigits = /^\d$/,
        size = 0,
        highestIdx = 0,
        len = 0;
    if (inputArr.hasOwnProperty('length')) {
        for (i = 1; i < argc; i++) {
            inputArr[inputArr.length] = argv[i];
        }
        return inputArr.length;
    }

    // Associative (object)
    for (pr in inputArr) {
        if (inputArr.hasOwnProperty(pr)) {
            ++len;
            if (pr.search(allDigits) !== -1) {
                size = parseInt(pr, 10);
                highestIdx = size > highestIdx ? size : highestIdx;
            }
        }
    }
    for (i = 1; i < argc; i++) {
        inputArr[++highestIdx] = argv[i];
    }
    return len + i - 1;
}

function array_shift(inputArr) {
    //  discuss at: http://phpjs.org/functions/array_shift/
    // original by: Kevin van Zonneveld (http://kevin.vanzonneveld.net)
    // improved by: Martijn Wieringa
    //        note: Currently does not handle objects
    //   example 1: array_shift(['Kevin', 'van', 'Zonneveld']);
    //   returns 1: 'Kevin'

    var props = false,
        shift = undefined,
        pr = '',
        allDigits = /^\d$/,
        int_ct = -1,
        _checkToUpIndices = function (arr, ct, key) {
            // Deal with situation, e.g., if encounter index 4 and try to set it to 0, but 0 exists later in loop (need to
            // increment all subsequent (skipping current key, since we need its value below) until find unused)
            if (arr[ct] !== undefined) {
                var tmp = ct;
                ct += 1;
                if (ct === key) {
                    ct += 1;
                }
                ct = _checkToUpIndices(arr, ct, key);
                arr[ct] = arr[tmp];
                delete arr[tmp];
            }
            return ct;
        };

    if (inputArr.length === 0) {
        return null;
    }
    if (inputArr.length > 0) {
        return inputArr.shift();
    }

    /*
     UNFINISHED FOR HANDLING OBJECTS
     for (pr in inputArr) {
     if (inputArr.hasOwnProperty(pr)) {
     props = true;
     shift = inputArr[pr];
     delete inputArr[pr];
     break;
     }
     }
     for (pr in inputArr) {
     if (inputArr.hasOwnProperty(pr)) {
     if (pr.search(allDigits) !== -1) {
     int_ct += 1;
     if (parseInt(pr, 10) === int_ct) {
     // Key is already numbered ok, so don't need to change key for value
     continue;
     }
     _checkToUpIndices(inputArr, int_ct, pr);
     arr[int_ct] = arr[pr];
     delete arr[pr];
     }
     }
     }
     if (!props) {
     return null;
     }
     return shift;
     */
}