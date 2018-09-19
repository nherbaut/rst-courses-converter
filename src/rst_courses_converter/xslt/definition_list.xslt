<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

    <xsl:output
            method="text"
            version="string"
            encoding="utf-8"
            omit-xml-declaration="yes"
            standalone="yes"
            doctype-public="string"
            doctype-system="string"
            cdata-section-elements="namelist"
            indent="no"
            media-type="string"/>
    <xsl:template match="//definition_list">

        <xsl:apply-templates/>
    </xsl:template>
    <xsl:template match="//definition_list"> &#x003E; **Définitions**
<xsl:for-each select="definition_list_item"> &#x003E; * **<xsl:value-of select="./term/text()"/>** : <xsl:value-of select="./definition/paragraph/text()"/> <xsl:value-of select="./definition/paragraph/reference/text()"/> <xsl:text>&#xa;</xsl:text>
        </xsl:for-each>
    </xsl:template>
</xsl:stylesheet>
