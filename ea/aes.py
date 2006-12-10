# -*- coding: utf-8 -*-

""" Battlefield 2142 Auth token encoder
This is the python module for creating auth tokens of EA/IGN's stat server.
"""

### some mimic functions to deal with Tubar's table and functions

def xorBYTE(a,b):
    """ Apply XOR to two char args """
    return chr( ord(a) ^ ord(b) )

def map_xor(*args):
    """ Char-by-char XOR of argument strings
    map-version: looks like it is a bit quickier
    """
    return ''.join(
        map( chr,
        map( lambda items: reduce(lambda x,y: x^y, items),
        zip( *map(lambda arg: map(ord,arg),args)))))

def lc_xor(*args):
    """ char-by-char XOR of argument strings.
    just working one (:
    """
    return ''.join([chr(byte) for byte in [ reduce(lambda x,y: x^y, items) for items in zip(*[[ ord(ch) for ch in arg] for arg in args])]])

xor = map_xor

#############################################################
# (o)riginal PHP code by Tubar from http://www.bfstats.info #
# Thank You, Tubar, for your great ea_support.php!          #
#############################################################

def getDWORD(s):
    """ Fetch four first bytes from string """
    return ''.join((s[3],s[2],s[1],s[0]))

def str2hex(s):
    """ Translate 'binary' string to it's hex-stream representation

    >>> hex2str('Mommy\x00')
    '4D6F6D6D7900'
    """
    return ''.join([hex(ord(char))[2:].rjust(2,'0') for char in s]).upper()

def hex2str(s):
    """ Translate hex-stream from string to character data

    >>> str2hex('AA56BB')
    '\xaa\x56\xbb'
    """
    return ''.join([chr(int( s[pos:pos+2], 16)) for pos in xrange(0,len(s),2)])

encryptKeys = map(hex2str, (
    'AA56BB4CC300007844EFFF652C2C1223',
    '8C27CA844F27CAFC0BC8359927E427BA',
    '78EBA34A37CC69B63C045C2F1BE07B95',
    '5244426F65882BD9598C77F6426C0C63',
    'A9681299CCE03940956C4EB6D70042D5',
    'AA6671A5668648E5F3EA065324EA4486',
    'EE50F69E88D6BE7B7B3CB8285FD6FCAE',
    '0A9F006E8249BE15F975063DA6A3FA93',
    'D6BB0AC354F2B4D6AD87B2EB0B244878',
    '6A903C8A3E62885C93E53AB798C172CF',
    'E0D644FCDEB4CCA04D51F617D59084D8',))

decryptKeys = map(hex2str, (
    'E0D644FCDEB4CCA04D51F617D59084D8',
    'E80D268FB0860DB32B386F8736CE0F13',
    '5269DD42588B2B3C9BBE62341DF66094',
    '88256F390AE2F67EC3354908864802A0',
    '521EFD6782C79947C9D7BF76457D4BA8',
    '2D1CC6EFD0D964204B1026318CAAF4DE',
    '3F341051FDC5A2CF9BC94211C7BAD2EF',
    '903CF661C2F1B29E660CE0DE5C7390FE',
    'DAE3F5B652CD44FFA4FD52403A7F7020',
    '135C842E882EB149F63016BF9E822260',
    'AA56BB4CC300007844EFFF652C2C1223',))

SBox = hex2str(
    '637C777BF26B6FC53001672BFED7AB76CA82C97DFA5947F0ADD4A2AF9CA472C0' \
    'B7FD9326363FF7CC34A5E5F171D8311504C723C31896059A071280E2EB27B275' \
    '09832C1A1B6E5AA0523BD6B329E32F8453D100ED20FCB15B6ACBBE394A4C58CF' \
    'D0EFAAFB434D338545F9027F503C9FA851A3408F929D38F5BCB6DA2110FFF3D2' \
    'CD0C13EC5F974417C4A77E3D645D197360814FDC222A908846EEB814DE5E0BDB' \
    'E0323A0A4906245CC2D3AC629195E479E7C8376D8DD54EA96C56F4EA657AAE08' \
    'BA78252E1CA6B4C6E8DD741F4BBD8B8A703EB5664803F60E613557B986C11D9E' \
    'E1F8981169D98E949B1E87E9CE5528DF8CA1890DBFE6426841992D0FB054BB16' )

SBoxInv = hex2str(
    '52096AD53036A538BF40A39E81F3D7FB7CE339829B2FFF87348E4344C4DEE9CB' \
    '547B9432A6C2233DEE4C950B42FAC34E082EA16628D924B2765BA2496D8BD125' \
    '72F8F66486689816D4A45CCC5D65B6926C704850FDEDB9DA5E154657A78D9D84' \
    '90D8AB008CBCD30AF7E45805B8B34506D02C1E8FCA3F0F02C1AFBD0301138A6B' \
    '3A9111414F67DCEA97F2CFCEF0B4E67396AC7422E7AD3585E2F937E81C75DF6E' \
    '47F11A711D29C5896FB7620EAA18BE1BFC563E4BC6D279209ADBC0FE78CD5AF4' \
    '1FDDA8338807C731B11210592780EC5F60517FA919B54A0D2DE57A9F93C99CEF' \
    'A0E03B4DAE2AF5B0C8EBBB3C83539961172B047EBA77D626E169146355210C7D' )

hashSm = (
    '',
    hex2str(
    'A56363C6847C7CF8997777EE8D7B7BF60DF2F2FFBD6B6BD6B16F6FDE54C5C591' \
    '5030306003010102A96767CE7D2B2B5619FEFEE762D7D7B5E6ABAB4D9A7676EC' \
    '45CACA8F9D82821F40C9C989877D7DFA15FAFAEFEB5959B2C947478E0BF0F0FB' \
    'ECADAD4167D4D4B3FDA2A25FEAAFAF45BF9C9C23F7A4A453967272E45BC0C09B' \
    'C2B7B7751CFDFDE1AE93933D6A26264C5A36366C413F3F7E02F7F7F54FCCCC83' \
    '5C343468F4A5A55134E5E5D108F1F1F9937171E273D8D8AB533131623F15152A' \
    '0C04040852C7C795652323465EC3C39D28181830A19696370F05050AB59A9A2F' \
    '0907070E361212249B80801B3DE2E2DF26EBEBCD6927274ECDB2B27F9F7575EA' \
    '1B0909129E83831D742C2C582E1A1A342D1B1B36B26E6EDCEE5A5AB4FBA0A05B' \
    'F65252A44D3B3B7661D6D6B7CEB3B37D7B2929523EE3E3DD712F2F5E97848413' \
    'F55353A668D1D1B9000000002CEDEDC1602020401FFCFCE3C8B1B179ED5B5BB6' \
    'BE6A6AD446CBCB8DD9BEBE674B393972DE4A4A94D44C4C98E85858B04ACFCF85' \
    '6BD0D0BB2AEFEFC5E5AAAA4F16FBFBEDC5434386D74D4D9A5533336694858511' \
    'CF45458A10F9F9E906020204817F7FFEF05050A0443C3C78BA9F9F25E3A8A84B' \
    'F35151A2FEA3A35DC04040808A8F8F05AD92923FBC9D9D214838387004F5F5F1' \
    'DFBCBC63C1B6B67775DADAAF63212142301010201AFFFFE50EF3F3FD6DD2D2BF' \
    '4CCDCD81140C0C18351313262FECECC3E15F5FBEA2979735CC4444883917172E' \
    '57C4C493F2A7A755827E7EFC473D3D7AAC6464C8E75D5DBA2B191932957373E6' \
    'A06060C098818119D14F4F9E7FDCDCA3662222447E2A2A54AB90903B8388880B' \
    'CA46468C29EEEEC7D3B8B86B3C14142879DEDEA7E25E5EBC1D0B0B1676DBDBAD' \
    '3BE0E0DB563232644E3A3A741E0A0A14DB4949920A06060C6C242448E45C5CB8' \
    '5DC2C29F6ED3D3BDEFACAC43A66262C4A8919139A495953137E4E4D38B7979F2' \
    '32E7E7D543C8C88B5937376EB76D6DDA8C8D8D0164D5D5B1D24E4E9CE0A9A949' \
    'B46C6CD8FA5656AC07F4F4F325EAEACFAF6565CA8E7A7AF4E9AEAE4718080810' \
    'D5BABA6F887878F06F25254A722E2E5C241C1C38F1A6A657C7B4B47351C6C697' \
    '23E8E8CB7CDDDDA19C7474E8211F1F3EDD4B4B96DCBDBD61868B8B0D858A8A0F' \
    '907070E0423E3E7CC4B5B571AA6666CCD84848900503030601F6F6F7120E0E1C' \
    'A36161C25F35356AF95757AED0B9B9699186861758C1C199271D1D3AB99E9E27' \
    '38E1E1D913F8F8EBB398982B33111122BB6969D270D9D9A9898E8E07A7949433' \
    'B69B9B2D221E1E3C9287871520E9E9C949CECE87FF5555AA782828507ADFDFA5' \
    '8F8C8C03F8A1A15980898909170D0D1ADABFBF6531E6E6D7C6424284B86868D0' \
    'C3414182B0999929772D2D5A110F0F1ECBB0B07BFC5454A8D6BBBB6D3A16162C' ),

    hex2str(
    '6363C6A57C7CF8847777EE997B7BF68DF2F2FF0D6B6BD6BD6F6FDEB1C5C59154' \
    '30306050010102036767CEA92B2B567DFEFEE719D7D7B562ABAB4DE67676EC9A' \
    'CACA8F4582821F9DC9C989407D7DFA87FAFAEF155959B2EB47478EC9F0F0FB0B' \
    'ADAD41ECD4D4B367A2A25FFDAFAF45EA9C9C23BFA4A453F77272E496C0C09B5B' \
    'B7B775C2FDFDE11C93933DAE26264C6A36366C5A3F3F7E41F7F7F502CCCC834F' \
    '3434685CA5A551F4E5E5D134F1F1F9087171E293D8D8AB733131625315152A3F' \
    '0404080CC7C7955223234665C3C39D5E18183028969637A105050A0F9A9A2FB5' \
    '07070E091212243680801B9BE2E2DF3DEBEBCD2627274E69B2B27FCD7575EA9F' \
    '0909121B83831D9E2C2C58741A1A342E1B1B362D6E6EDCB25A5AB4EEA0A05BFB' \
    '5252A4F63B3B764DD6D6B761B3B37DCE2929527BE3E3DD3E2F2F5E7184841397' \
    '5353A6F5D1D1B96800000000EDEDC12C20204060FCFCE31FB1B179C85B5BB6ED' \
    '6A6AD4BECBCB8D46BEBE67D93939724B4A4A94DE4C4C98D45858B0E8CFCF854A' \
    'D0D0BB6BEFEFC52AAAAA4FE5FBFBED16434386C54D4D9AD73333665585851194' \
    '45458ACFF9F9E910020204067F7FFE815050A0F03C3C78449F9F25BAA8A84BE3' \
    '5151A2F3A3A35DFE404080C08F8F058A92923FAD9D9D21BC38387048F5F5F104' \
    'BCBC63DFB6B677C1DADAAF752121426310102030FFFFE51AF3F3FD0ED2D2BF6D' \
    'CDCD814C0C0C181413132635ECECC32F5F5FBEE1979735A2444488CC17172E39' \
    'C4C49357A7A755F27E7EFC823D3D7A476464C8AC5D5DBAE71919322B7373E695' \
    '6060C0A0818119984F4F9ED1DCDCA37F222244662A2A547E90903BAB88880B83' \
    '46468CCAEEEEC729B8B86BD31414283CDEDEA7795E5EBCE20B0B161DDBDBAD76' \
    'E0E0DB3B323264563A3A744E0A0A141E494992DB06060C0A2424486C5C5CB8E4' \
    'C2C29F5DD3D3BD6EACAC43EF6262C4A6919139A8959531A4E4E4D3377979F28B' \
    'E7E7D532C8C88B4337376E596D6DDAB78D8D018CD5D5B1644E4E9CD2A9A949E0' \
    '6C6CD8B45656ACFAF4F4F307EAEACF256565CAAF7A7AF48EAEAE47E908081018' \
    'BABA6FD57878F08825254A6F2E2E5C721C1C3824A6A657F1B4B473C7C6C69751' \
    'E8E8CB23DDDDA17C7474E89C1F1F3E214B4B96DDBDBD61DC8B8B0D868A8A0F85' \
    '7070E0903E3E7C42B5B571C46666CCAA484890D803030605F6F6F7010E0E1C12' \
    '6161C2A335356A5F5757AEF9B9B969D086861791C1C199581D1D3A279E9E27B9' \
    'E1E1D938F8F8EB1398982BB3111122336969D2BBD9D9A9708E8E0789949433A7' \
    '9B9B2DB61E1E3C2287871592E9E9C920CECE87495555AAFF28285078DFDFA57A' \
    '8C8C038FA1A159F8898909800D0D1A17BFBF65DAE6E6D731424284C66868D0B8' \
    '414182C3999929B02D2D5A770F0F1E11B0B07BCB5454A8FCBBBB6DD616162C3A' ),
    hex2str(
    '63C6A5637CF8847C77EE99777BF68D7BF2FF0DF26BD6BD6B6FDEB16FC59154C5' \
    '306050300102030167CEA9672B567D2BFEE719FED7B562D7AB4DE6AB76EC9A76' \
    'CA8F45CA821F9D82C98940C97DFA877DFAEF15FA59B2EB59478EC947F0FB0BF0' \
    'AD41ECADD4B367D4A25FFDA2AF45EAAF9C23BF9CA453F7A472E49672C09B5BC0' \
    'B775C2B7FDE11CFD933DAE93264C6A26366C5A363F7E413FF7F502F7CC834FCC' \
    '34685C34A551F4A5E5D134E5F1F908F171E29371D8AB73D831625331152A3F15' \
    '04080C04C79552C723466523C39D5EC3183028189637A196050A0F059A2FB59A' \
    '070E090712243612801B9B80E2DF3DE2EBCD26EB274E6927B27FCDB275EA9F75' \
    '09121B09831D9E832C58742C1A342E1A1B362D1B6EDCB26E5AB4EE5AA05BFBA0' \
    '52A4F6523B764D3BD6B761D6B37DCEB329527B29E3DD3EE32F5E712F84139784' \
    '53A6F553D1B968D100000000EDC12CED20406020FCE31FFCB179C8B15BB6ED5B' \
    '6AD4BE6ACB8D46CBBE67D9BE39724B394A94DE4A4C98D44C58B0E858CF854ACF' \
    'D0BB6BD0EFC52AEFAA4FE5AAFBED16FB4386C5434D9AD74D3366553385119485' \
    '458ACF45F9E910F9020406027FFE817F50A0F0503C78443C9F25BA9FA84BE3A8' \
    '51A2F351A35DFEA34080C0408F058A8F923FAD929D21BC9D38704838F5F104F5' \
    'BC63DFBCB677C1B6DAAF75DA2142632110203010FFE51AFFF3FD0EF3D2BF6DD2' \
    'CD814CCD0C18140C13263513ECC32FEC5FBEE15F9735A2974488CC44172E3917' \
    'C49357C4A755F2A77EFC827E3D7A473D64C8AC645DBAE75D19322B1973E69573' \
    '60C0A060811998814F9ED14FDCA37FDC224466222A547E2A903BAB90880B8388' \
    '468CCA46EEC729EEB86BD3B814283C14DEA779DE5EBCE25E0B161D0BDBAD76DB' \
    'E0DB3BE0326456323A744E3A0A141E0A4992DB49060C0A0624486C245CB8E45C' \
    'C29F5DC2D3BD6ED3AC43EFAC62C4A6629139A8919531A495E4D337E479F28B79' \
    'E7D532E7C88B43C8376E59376DDAB76D8D018C8DD5B164D54E9CD24EA949E0A9' \
    '6CD8B46C56ACFA56F4F307F4EACF25EA65CAAF657AF48E7AAE47E9AE08101808' \
    'BA6FD5BA78F08878254A6F252E5C722E1C38241CA657F1A6B473C7B4C69751C6' \
    'E8CB23E8DDA17CDD74E89C741F3E211F4B96DD4BBD61DCBD8B0D868B8A0F858A' \
    '70E090703E7C423EB571C4B566CCAA664890D84803060503F6F701F60E1C120E' \
    '61C2A361356A5F3557AEF957B969D0B986179186C19958C11D3A271D9E27B99E' \
    'E1D938E1F8EB13F8982BB3981122331169D2BB69D9A970D98E07898E9433A794' \
    '9B2DB69B1E3C221E87159287E9C920E9CE8749CE55AAFF5528507828DFA57ADF' \
    '8C038F8CA159F8A1890980890D1A170DBF65DABFE6D731E64284C64268D0B868' \
    '4182C3419929B0992D5A772D0F1E110FB07BCBB054A8FC54BB6DD6BB162C3A16' ),
    hex2str(
    'C6A56363F8847C7CEE997777F68D7B7BFF0DF2F2D6BD6B6BDEB16F6F9154C5C5' \
    '6050303002030101CEA96767567D2B2BE719FEFEB562D7D74DE6ABABEC9A7676' \
    '8F45CACA1F9D82828940C9C9FA877D7DEF15FAFAB2EB59598EC94747FB0BF0F0' \
    '41ECADADB367D4D45FFDA2A245EAAFAF23BF9C9C53F7A4A4E49672729B5BC0C0' \
    '75C2B7B7E11CFDFD3DAE93934C6A26266C5A36367E413F3FF502F7F7834FCCCC' \
    '685C343451F4A5A5D134E5E5F908F1F1E2937171AB73D8D8625331312A3F1515' \
    '080C04049552C7C7466523239D5EC3C33028181837A196960A0F05052FB59A9A' \
    '0E090707243612121B9B8080DF3DE2E2CD26EBEB4E6927277FCDB2B2EA9F7575' \
    '121B09091D9E838358742C2C342E1A1A362D1B1BDCB26E6EB4EE5A5A5BFBA0A0' \
    'A4F65252764D3B3BB761D6D67DCEB3B3527B2929DD3EE3E35E712F2F13978484' \
    'A6F55353B968D1D100000000C12CEDED40602020E31FFCFC79C8B1B1B6ED5B5B' \
    'D4BE6A6A8D46CBCB67D9BEBE724B393994DE4A4A98D44C4CB0E85858854ACFCF' \
    'BB6BD0D0C52AEFEF4FE5AAAAED16FBFB86C543439AD74D4D6655333311948585' \
    '8ACF4545E910F9F904060202FE817F7FA0F0505078443C3C25BA9F9F4BE3A8A8' \
    'A2F351515DFEA3A380C04040058A8F8F3FAD929221BC9D9D70483838F104F5F5' \
    '63DFBCBC77C1B6B6AF75DADA4263212120301010E51AFFFFFD0EF3F3BF6DD2D2' \
    '814CCDCD18140C0C26351313C32FECECBEE15F5F35A2979788CC44442E391717' \
    '9357C4C455F2A7A7FC827E7E7A473D3DC8AC6464BAE75D5D322B1919E6957373' \
    'C0A06060199881819ED14F4FA37FDCDC44662222547E2A2A3BAB90900B838888' \
    '8CCA4646C729EEEE6BD3B8B8283C1414A779DEDEBCE25E5E161D0B0BAD76DBDB' \
    'DB3BE0E064563232744E3A3A141E0A0A92DB49490C0A0606486C2424B8E45C5C' \
    '9F5DC2C2BD6ED3D343EFACACC4A6626239A8919131A49595D337E4E4F28B7979' \
    'D532E7E78B43C8C86E593737DAB76D6D018C8D8DB164D5D59CD24E4E49E0A9A9' \
    'D8B46C6CACFA5656F307F4F4CF25EAEACAAF6565F48E7A7A47E9AEAE10180808' \
    '6FD5BABAF08878784A6F25255C722E2E38241C1C57F1A6A673C7B4B49751C6C6' \
    'CB23E8E8A17CDDDDE89C74743E211F1F96DD4B4B61DCBDBD0D868B8B0F858A8A' \
    'E09070707C423E3E71C4B5B5CCAA666690D8484806050303F701F6F61C120E0E' \
    'C2A361616A5F3535AEF9575769D0B9B9179186869958C1C13A271D1D27B99E9E' \
    'D938E1E1EB13F8F82BB3989822331111D2BB6969A970D9D907898E8E33A79494' \
    '2DB69B9B3C221E1E15928787C920E9E98749CECEAAFF555550782828A57ADFDF' \
    '038F8C8C59F8A1A1098089891A170D0D65DABFBFD731E6E684C64242D0B86868' \
    '82C3414129B099995A772D2D1E110F0F7BCBB0B0A8FC54546DD6BBBB2C3A1616' ),
    
    # Code5,6,7,8 are used for decoding

    hex2str(
    '50A7F4515365417EC3A4171A965E273ACB6BAB3BF1459D1FAB58FAAC9303E34B' \
    '55FA3020F66D76AD9176CC88254C02F5FCD7E54FD7CB2AC5804435268FA362B5' \
    '495AB1DE671BBA25980EEA45E1C0FE5D02752FC312F04C81A397468DC6F9D36B' \
    'E75F8F03959C9215EB7A6DBFDA5952952D83BED4D32174582969E04944C8C98E' \
    '6A89C27578798EF46B3E5899DD71B927B64FE1BE17AD88F066AC20C9B43ACE7D' \
    '184ADF6382311AE560335197457F5362E07764B184AE6BBB1CA081FE942B08F9' \
    '5868487019FD458F876CDE94B7F87B5223D373ABE2024B72578F1FE32AAB5566' \
    '0728EBB203C2B52F9A7BC586A50837D3F2872830B2A5BF23BA6A03025C8216ED' \
    '2B1CCF8A92B479A7F0F207F3A1E2694ECDF4DA65D5BE05061F6234D18AFEA6C4' \
    '9D532E34A055F3A232E18A0575EBF6A439EC830BAAEF6040069F715E51106EBD' \
    'F98A213E3D06DD96AE053EDD46BDE64DB58D5491055DC4716FD40604FF155060' \
    '24FB981997E9BDD6CC434089779ED967BD42E8B0888B8907385B19E7DBEEC879' \
    '470A7CA1E90F427CC91E84F8000000008386800948ED2B32AC70111E4E725A6C' \
    'FBFF0EFD5638850F1ED5AE3D27392D3664D90F0A21A65C68D1545B9B3A2E3624' \
    'B1670A0C0FE75793D296EEB49E919B1B4FC5C080A220DC61694B775A161A121C' \
    '0ABA93E2E52AA0C043E0223C1D171B120B0D090EADC78BF2B9A8B62DC8A91E14' \
    '8519F1574C0775AFBBDD99EEFD607FA39F2601F7BCF5725CC53B6644347EFB5B' \
    '7629438BDCC623CB68FCEDB663F1E4B8CADC31D710856342402297132011C684' \
    '7D244A85F83DBBD21132F9AE6DA129C74B2F9E1DF330B2DCEC52860DD0E3C177' \
    '6C16B32B99B970A9FA4894112264E947C48CFCA81A3FF0A0D82C7D56EF903322' \
    'C74E4987C1D138D9FEA2CA8C360BD498CF81F5A628DE7AA5268EB7DAA4BFAD3F' \
    'E49D3A2C0D9278509BCC5F6A62467E54C2138DF6E8B8D8905EF7392EF5AFC382' \
    'BE805D9F7C93D069A92DD56FB31225CF3B99ACC8A77D18106E639CE87BBB3BDB' \
    '097826CDF418596E01B79AECA89A4F83656E95E67EE6FFAA08CFBC21E6E815EF' \
    'D99BE7BACE366F4AD4099FEAD67CB029AFB2A43131233F2A3094A5C6C066A235' \
    '37BC4E74A6CA82FCB0D090E015D8A7334A9804F1F7DAEC410E50CD7F2FF69117' \
    '8DD64D764DB0EF43544DAACCDF0496E4E3B5D19E1B886A4CB81F2CC17F516546' \
    '04EA5E9D5D358C01737487FA2E410BFB5A1D67B352D2DB92335610E91347D66D' \
    '8C61D79A7A0CA1378E14F859893C13EBEE27A9CE35C961B7EDE51CE13CB1477A' \
    '59DFD29C3F73F25579CE1418BF37C773EACDF7535BAAFD5F146F3DDF86DB4478' \
    '81F3AFCA3EC468B92C3424385F40A3C272C31D160C25E2BC8B493C2841950DFF' \
    '7101A839DEB30C089CE4B4D890C156646184CB7B70B632D5745C6C484257B8D0' ),
    hex2str(
    'A7F4515065417E53A4171AC35E273A966BAB3BCB459D1FF158FAACAB03E34B93' \
    'FA3020556D76ADF676CC88914C02F525D7E54FFCCB2AC5D744352680A362B58F' \
    '5AB1DE491BBA25670EEA4598C0FE5DE1752FC302F04C811297468DA3F9D36BC6' \
    '5F8F03E79C9215957A6DBFEB595295DA83BED42D217458D369E04929C8C98E44' \
    '89C2756A798EF4783E58996B71B927DD4FE1BEB6AD88F017AC20C9663ACE7DB4' \
    '4ADF6318311AE582335197607F5362457764B1E0AE6BBB84A081FE1C2B08F994' \
    '68487058FD458F196CDE9487F87B52B7D373AB23024B72E28F1FE357AB55662A' \
    '28EBB207C2B52F037BC5869A0837D3A5872830F2A5BF23B26A0302BA8216ED5C' \
    '1CCF8A2BB479A792F207F3F0E2694EA1F4DA65CDBE0506D56234D11FFEA6C48A' \
    '532E349D55F3A2A0E18A0532EBF6A475EC830B39EF6040AA9F715E06106EBD51' \
    '8A213EF906DD963D053EDDAEBDE64D468D5491B55DC47105D406046F155060FF' \
    'FB981924E9BDD697434089CC9ED9677742E8B0BD8B8907885B19E738EEC879DB' \
    '0A7CA1470F427CE91E84F8C90000000086800983ED2B324870111EAC725A6C4E' \
    'FF0EFDFB38850F56D5AE3D1E392D3627D90F0A64A65C6821545B9BD12E36243A' \
    '670A0CB1E757930F96EEB4D2919B1B9EC5C0804F20DC61A24B775A691A121C16' \
    'BA93E20A2AA0C0E5E0223C43171B121D0D090E0BC78BF2ADA8B62DB9A91E14C8' \
    '19F157850775AF4CDD99EEBB607FA3FD2601F79FF5725CBC3B6644C57EFB5B34' \
    '29438B76C623CBDCFCEDB668F1E4B863DC31D7CA856342102297134011C68420' \
    '244A857D3DBBD2F832F9AE11A129C76D2F9E1D4B30B2DCF352860DECE3C177D0' \
    '16B32B6CB970A999489411FA64E947228CFCA8C43FF0A01A2C7D56D8903322EF' \
    '4E4987C7D138D9C1A2CA8CFE0BD4983681F5A6CFDE7AA5288EB7DA26BFAD3FA4' \
    '9D3A2CE49278500DCC5F6A9B467E5462138DF6C2B8D890E8F7392E5EAFC382F5' \
    '805D9FBE93D0697C2DD56FA91225CFB399ACC83B7D1810A7639CE86EBB3BDB7B' \
    '7826CD0918596EF4B79AEC019A4F83A86E95E665E6FFAA7ECFBC2108E815EFE6' \
    '9BE7BAD9366F4ACE099FEAD47CB029D6B2A431AF233F2A3194A5C63066A235C0' \
    'BC4E7437CA82FCA6D090E0B0D8A733159804F14ADAEC41F750CD7F0EF691172F' \
    'D64D768DB0EF434D4DAACC540496E4DFB5D19EE3886A4C1B1F2CC1B85165467F' \
    'EA5E9D04358C015D7487FA73410BFB2E1D67B35AD2DB92525610E93347D66D13' \
    '61D79A8C0CA1377A14F8598E3C13EB8927A9CEEEC961B735E51CE1EDB1477A3C' \
    'DFD29C5973F2553FCE14187937C773BFCDF753EAAAFD5F5B6F3DDF14DB447886' \
    'F3AFCA81C468B93E3424382C40A3C25FC31D167225E2BC0C493C288B950DFF41' \
    '01A83971B30C08DEE4B4D89CC156649084CB7B61B632D5705C6C487457B8D042' ),
    hex2str(
    'F45150A7417E5365171AC3A4273A965EAB3BCB6B9D1FF145FAACAB58E34B9303' \
    '302055FA76ADF66DCC88917602F5254CE54FFCD72AC5D7CB3526804462B58FA3' \
    'B1DE495ABA25671BEA45980EFE5DE1C02FC302754C8112F0468DA397D36BC6F9' \
    '8F03E75F9215959C6DBFEB7A5295DA59BED42D837458D321E0492969C98E44C8' \
    'C2756A898EF4787958996B3EB927DD71E1BEB64F88F017AD20C966ACCE7DB43A' \
    'DF63184A1AE58231519760335362457F64B1E0776BBB84AE81FE1CA008F9942B' \
    '48705868458F19FDDE94876C7B52B7F873AB23D34B72E2021FE3578F55662AAB' \
    'EBB20728B52F03C2C5869A7B37D3A5082830F287BF23B2A50302BA6A16ED5C82' \
    'CF8A2B1C79A792B407F3F0F2694EA1E2DA65CDF40506D5BE34D11F62A6C48AFE' \
    '2E349D53F3A2A0558A0532E1F6A475EB830B39EC6040AAEF715E069F6EBD5110' \
    '213EF98ADD963D063EDDAE05E64D46BD5491B58DC471055D06046FD45060FF15' \
    '981924FBBDD697E94089CC43D967779EE8B0BD428907888B19E7385BC879DBEE' \
    '7CA1470A427CE90F84F8C91E00000000800983862B3248ED111EAC705A6C4E72' \
    '0EFDFBFF850F5638AE3D1ED52D3627390F0A64D95C6821A65B9BD15436243A2E' \
    '0A0CB16757930FE7EEB4D2969B1B9E91C0804FC5DC61A220775A694B121C161A' \
    '93E20ABAA0C0E52A223C43E01B121D17090E0B0D8BF2ADC7B62DB9A81E14C8A9' \
    'F157851975AF4C0799EEBBDD7FA3FD6001F79F26725CBCF56644C53BFB5B347E' \
    '438B762923CBDCC6EDB668FCE4B863F131D7CADC6342108597134022C6842011' \
    '4A857D24BBD2F83DF9AE113229C76DA19E1D4B2FB2DCF330860DEC52C177D0E3' \
    'B32B6C1670A999B99411FA48E9472264FCA8C48CF0A01A3F7D56D82C3322EF90' \
    '4987C74E38D9C1D1CA8CFEA2D498360BF5A6CF817AA528DEB7DA268EAD3FA4BF' \
    '3A2CE49D78500D925F6A9BCC7E5462468DF6C213D890E8B8392E5EF7C382F5AF' \
    '5D9FBE80D0697C93D56FA92D25CFB312ACC83B991810A77D9CE86E633BDB7BBB' \
    '26CD0978596EF4189AEC01B74F83A89A95E6656EFFAA7EE6BC2108CF15EFE6E8' \
    'E7BAD99B6F4ACE369FEAD409B029D67CA431AFB23F2A3123A5C63094A235C066' \
    '4E7437BC82FCA6CA90E0B0D0A73315D804F14A98EC41F7DACD7F0E5091172FF6' \
    '4D768DD6EF434DB0AACC544D96E4DF04D19EE3B56A4C1B882CC1B81F65467F51' \
    '5E9D04EA8C015D3587FA73740BFB2E4167B35A1DDB9252D210E93356D66D1347' \
    'D79A8C61A1377A0CF8598E1413EB893CA9CEEE2761B735C91CE1EDE5477A3CB1' \
    'D29C59DFF2553F73141879CEC773BF37F753EACDFD5F5BAA3DDF146F447886DB' \
    'AFCA81F368B93EC424382C34A3C25F401D1672C3E2BC0C253C288B490DFF4195' \
    'A83971010C08DEB3B4D89CE4566490C1CB7B618432D570B66C48745CB8D04257' ),
    hex2str(
    '5150A7F47E5365411AC3A4173A965E273BCB6BAB1FF1459DACAB58FA4B9303E3' \
    '2055FA30ADF66D76889176CCF5254C024FFCD7E5C5D7CB2A26804435B58FA362' \
    'DE495AB125671BBA45980EEA5DE1C0FEC302752F8112F04C8DA397466BC6F9D3' \
    '03E75F8F15959C92BFEB7A6D95DA5952D42D83BE58D32174492969E08E44C8C9' \
    '756A89C2F478798E996B3E5827DD71B9BEB64FE1F017AD88C966AC207DB43ACE' \
    '63184ADFE582311A9760335162457F53B1E07764BB84AE6BFE1CA081F9942B08' \
    '705868488F19FD4594876CDE52B7F87BAB23D37372E2024BE3578F1F662AAB55' \
    'B20728EB2F03C2B5869A7BC5D3A5083730F2872823B2A5BF02BA6A03ED5C8216' \
    '8A2B1CCFA792B479F3F0F2074EA1E26965CDF4DA06D5BE05D11F6234C48AFEA6' \
    '349D532EA2A055F30532E18AA475EBF60B39EC8340AAEF605E069F71BD51106E' \
    '3EF98A21963D06DDDDAE053E4D46BDE691B58D5471055DC4046FD40660FF1550' \
    '1924FB98D697E9BD89CC434067779ED9B0BD42E807888B89E7385B1979DBEEC8' \
    'A1470A7C7CE90F42F8C91E8400000000098386803248ED2B1EAC70116C4E725A' \
    'FDFBFF0E0F5638853D1ED5AE3627392D0A64D90F6821A65C9BD1545B243A2E36' \
    '0CB1670A930FE757B4D296EE1B9E919B804FC5C061A220DC5A694B771C161A12' \
    'E20ABA93C0E52AA03C43E022121D171B0E0B0D09F2ADC78B2DB9A8B614C8A91E' \
    '578519F1AF4C0775EEBBDD99A3FD607FF79F26015CBCF57244C53B665B347EFB' \
    '8B762943CBDCC623B668FCEDB863F1E4D7CADC314210856313402297842011C6' \
    '857D244AD2F83DBBAE1132F9C76DA1291D4B2F9EDCF330B20DEC528677D0E3C1' \
    '2B6C16B3A999B97011FA4894472264E9A8C48CFCA01A3FF056D82C7D22EF9033' \
    '87C74E49D9C1D1388CFEA2CA98360BD4A6CF81F5A528DE7ADA268EB73FA4BFAD' \
    '2CE49D3A500D92786A9BCC5F5462467EF6C2138D90E8B8D82E5EF73982F5AFC3' \
    '9FBE805D697C93D06FA92DD5CFB31225C83B99AC10A77D18E86E639CDB7BBB3B' \
    'CD0978266EF41859EC01B79A83A89A4FE6656E95AA7EE6FF2108CFBCEFE6E815' \
    'BAD99BE74ACE366FEAD4099F29D67CB031AFB2A42A31233FC63094A535C066A2' \
    '7437BC4EFCA6CA82E0B0D0903315D8A7F14A980441F7DAEC7F0E50CD172FF691' \
    '768DD64D434DB0EFCC544DAAE4DF04969EE3B5D14C1B886AC1B81F2C467F5165' \
    '9D04EA5E015D358CFA737487FB2E410BB35A1D679252D2DBE93356106D1347D6' \
    '9A8C61D7377A0CA1598E14F8EB893C13CEEE27A9B735C961E1EDE51C7A3CB147' \
    '9C59DFD2553F73F21879CE1473BF37C753EACDF75F5BAAFDDF146F3D7886DB44' \
    'CA81F3AFB93EC468382C3424C25F40A31672C31DBC0C25E2288B493CFF41950D' \
    '397101A808DEB30CD89CE4B46490C1567B6184CBD570B63248745C6CD04257B8' ),
)

def getKeyDWORD(key, idx):
    """ Get a DWORD from key table. """
    pos = idx*4
    return getDWORD(key[pos:pos+4])

def getSmDWORD(tab, idx):
    """ Get a DWORD from Sm table. """
    pos = ord(idx) * 4
    return getDWORD(hashSm[tab][pos:pos+4])

def getKeyBYTE(key, idx):
    """ Get a BYTE from key string """
    return key[ord(idx)]

def DefEncryptBlock(inp):
    """ Encrypt the 16 bytes of input string using EA's AES tables. """
    Ker = encryptKeys[0]

    t0 = xor(inp[0:4],   getKeyDWORD(Ker, 0))
    t1 = xor(inp[4:8],   getKeyDWORD(Ker, 1))
    t2 = xor(inp[8:12],  getKeyDWORD(Ker, 2))
    t3 = xor(inp[12:16], getKeyDWORD(Ker, 3))

#    print "T: %s %s %s %s" % (str2hex(t0), str2hex(t1), str2hex(t2), str2hex(t3))

    for r in xrange(1,10):
        Ker = encryptKeys[r]
#        print "R%d Ker: %s"  % (r, str2hex(Ker))
        a0 = xor( getSmDWORD(1, t0[0]),
                  getSmDWORD(2, t1[1]),
                  getSmDWORD(3, t2[2]),
                  getSmDWORD(4, t3[3]),
                  getKeyDWORD(Ker, 0)
                )
        a1 = xor( getSmDWORD(1, t1[0]),
                  getSmDWORD(2, t2[1]),
                  getSmDWORD(3, t3[2]),
                  getSmDWORD(4, t0[3]),
                  getKeyDWORD(Ker, 1)
                )
        a2 = xor( getSmDWORD(1, t2[0]),
                  getSmDWORD(2, t3[1]),
                  getSmDWORD(3, t0[2]),
                  getSmDWORD(4, t1[3]),
                  getKeyDWORD(Ker, 2)
                )
        a3 = xor( getSmDWORD(1, t3[0]),
                  getSmDWORD(2, t0[1]),
                  getSmDWORD(3, t1[2]),
                  getSmDWORD(4, t2[3]),
                  getKeyDWORD(Ker, 3)
                )
        t0, t1, t2, t3 = a0, a1, a2, a3
#        print "R[%d]: %s %s %s %s\n" % (r, str2hex(t0), str2hex(t1), str2hex(t2), str2hex(t3))

    Ker = encryptKeys[10]

    result = []
    tt = getKeyDWORD(Ker, 0)
    result.append( xorBYTE( getKeyBYTE(SBox, t0[0]), tt[0] ) )
    result.append( xorBYTE( getKeyBYTE(SBox, t1[1]), tt[1] ) )
    result.append( xorBYTE( getKeyBYTE(SBox, t2[2]), tt[2] ) )
    result.append( xorBYTE( getKeyBYTE(SBox, t3[3]), tt[3] ) )
    tt = getKeyDWORD(Ker, 1)
    result.append( xorBYTE( getKeyBYTE(SBox, t1[0]), tt[0] ) )
    result.append( xorBYTE( getKeyBYTE(SBox, t2[1]), tt[1] ) )
    result.append( xorBYTE( getKeyBYTE(SBox, t3[2]), tt[2] ) )
    result.append( xorBYTE( getKeyBYTE(SBox, t0[3]), tt[3] ) )
    tt = getKeyDWORD(Ker, 2)
    result.append( xorBYTE( getKeyBYTE(SBox, t2[0]), tt[0] ) )
    result.append( xorBYTE( getKeyBYTE(SBox, t3[1]), tt[1] ) )
    result.append( xorBYTE( getKeyBYTE(SBox, t0[2]), tt[2] ) )
    result.append( xorBYTE( getKeyBYTE(SBox, t1[3]), tt[3] ) )
    tt = getKeyDWORD(Ker, 3)
    result.append( xorBYTE( getKeyBYTE(SBox, t3[0]), tt[0] ) )
    result.append( xorBYTE( getKeyBYTE(SBox, t0[1]), tt[1] ) )
    result.append( xorBYTE( getKeyBYTE(SBox, t1[2]), tt[2] ) )
    result.append( xorBYTE( getKeyBYTE(SBox, t2[3]), tt[3] ) )

    return ''.join(result)
