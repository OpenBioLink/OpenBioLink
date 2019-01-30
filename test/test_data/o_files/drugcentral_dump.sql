ALTER TABLE IF EXISTS ONLY public.tdkey2tc DROP CONSTRAINT IF EXISTS tdgo2tc_2_tc;
ALTER TABLE IF EXISTS ONLY public.tdgo2tc DROP CONSTRAINT IF EXISTS tdgo2tc_2_tc;
ALTER TABLE IF EXISTS ONLY public.tdkey2tc DROP CONSTRAINT IF EXISTS tdgo2tc_2_kw;
ALTER TABLE IF EXISTS ONLY public.approval DROP CONSTRAINT IF EXISTS approval_2_struct;
ALTER TABLE IF EXISTS ONLY public.active_ingredient DROP CONSTRAINT IF EXISTS active_ingredient_ndc_product_code_fkey;
DROP INDEX IF EXISTS public.sql120404123859152;
DROP INDEX IF EXISTS public.sql120404123658531;
DROP INDEX IF EXISTS public.sql100501183943930;
ALTER TABLE IF EXISTS ONLY public.action_type DROP CONSTRAINT IF EXISTS sql141210123613761;
ALTER TABLE IF EXISTS ONLY public.action_type DROP CONSTRAINT IF EXISTS sql141210123613760;
ALTER TABLE IF EXISTS ONLY public.td2tc DROP CONSTRAINT IF EXISTS sql141205191436250;
ALTER TABLE IF EXISTS ONLY public.target_dictionary DROP CONSTRAINT IF EXISTS sql141205191111190;
COPY public.omop_relationship (id, struct_id, concept_id, relationship_name, concept_name, umls_cui, snomed_full_name, cui_semantic_type, snomed_conceptid) FROM stdin;
132491	101	21000703	indication	Hypertriglyceridemia	C0000001	Hypertriglyceridemia	T033	302870006
132492	102	21000705	indication	Mixed hyperlipidemia	C0000002	Mixed hyperlipidemia	T047	267434003
132493	101	40249217	indication	Chronic non-neuropathic Gaucher's disease	C0000002	Chronic non-neuropathic Gaucher's disease	T047	62201009
132496	661	40249309	reduce risk	Cardiovascular event	C6666661	Cardiovascular event	T033	405617006
133138	991	21000584	contraindication	Hypothyroidism	C0005000	Hypothyroidism	T047	40930008
133138	992	21000584	contraindication	Hypothyroidism	C0005000	Hypothyroidism	T047	40930008
133139	663	21013404	off-label use	Ventilator-acquired pneumonia	C6666663	Ventilator-acquired pneumonia	T047	429271009
\.


--
-- Data for Name: parentmol; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.parentmol (cd_id, name, cas_reg_no, inchi, nostereo_inchi, molfile, molimg, smiles, inchikey) FROM stdin;
221	Blood-coagulation factor VIII	113189-02-9	\N	\N	\N	\N	\N	\N
\.


--
-- Data for Name: identifier; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.identifier (id, identifier, id_type, struct_id, parent_match) FROM stdin;
1059443	7998	IUPHAR_LIGAND_ID	5246	\N
1059444	D10438	KEGG_DRUG	5246	\N
1168237	55	PUBCHEM_CID	101	\N
1168238	85	PUBCHEM_CID	992	\N
1168261	666663	PUBCHEM_CID	66666	\N
1175448	F0XDI6ZL63	UNII	2977	f
1175449	7778	INN_ID	2977	f
1175452	56109-02-5	SECONDARY_CAS_RN	3817	f
\.
